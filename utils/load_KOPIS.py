from urllib.request import urlopen, Request
import os, configparser, datetime
import mysql.connector
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs


# ST_DT = datetime.datetime.now()

config = configparser.ConfigParser()
config.read('config/config.ini')

SERVICE_KEY = config.get('KOPIS_KEYS', 'API_KEY')
MYSQL_HOST = config.get('MYSQL', 'MYSQL_HOST')
MYSQL_PWD = config.get('MYSQL', 'MYSQL_PWD')
MYSQL_PORT = config.get('MYSQL', 'MYSQL_PORT')
MYSQL_USER = config.get('MYSQL', 'MYSQL_USER')
MYSQL_DB = config.get('MYSQL', 'MYSQL_DB')


# conn = mysql.connector.connect(host=MYSQL_HOST, password=MYSQL_PWD, port=MYSQL_PORT, user=MYSQL_USER, database=MYSQL_DB)
conn = mysql.connector.connect(host='localhost', password='mysql0930', port=3306, user='root', database='culture')
cur = conn.cursor()

def get_ticket_page(code):
    url = f"https://www.kopis.or.kr/por/db/pblprfr/pblprfrView.do?menuId=MNU_00020&mt20Id={code}&search=db"

    response=urlopen(url)
    soup=bs(response,'html.parser')

    ticket_link=soup.find_all('div',class_='btnType01')

    ticket_nm=[]
    ticket_href=[]
    
    for ticket in ticket_link:
        href=ticket.find('a').get('href')
        txt=ticket.find('a').get_text()

        ticket_nm.append(txt)
        ticket_href.append(href)
    
    return ticket_nm, ticket_href

def get_mt20id(start_date): # end_date는 Dag에서 start_date(execution_date가 되겠지요?)기준 timedelta로 +4주로 계산

    config = configparser.ConfigParser()
    config.read('config/config.ini')
    


    CPAGE=1
    ROWS= '1'

    end_date= (start_date + datetime.timedelta(weeks=4)).strftime("%Y%m%d")
    start_date= start_date.strftime("%Y%m%d")
    print(start_date,end_date)

    url = f'http://www.kopis.or.kr/openApi/restful/prfper?service={SERVICE_KEY}&stdate={start_date}&eddate={end_date}&cpage={CPAGE}&rows={ROWS}'
    result = urlopen(url)
    data = bs(result, 'lxml-xml')
    db = data.find_all('db')
    # print(len(db))
    
    id=[]
    nm=[]
    author=[]
    creator=[]
    
    for pf in db :
        pf_id = pf.find('mt20id').text
        pf_nm = pf.find('prfnm').text

        try:
            pf_author = pf.find('author').text
        except:
            pf_author = pf.find('author')

        try:
            pf_creator = pf.find('creator').text
        except:
            pf_creator = pf.find('creator')

        id.append(pf_id)
        nm.append(pf_nm)
        author.append(pf_author)
        creator.append(pf_creator)


    data_dict={}

    data_dict['mt20id']=id
    data_dict['name']=nm
    data_dict['author']=author
    data_dict['creator']=creator

    for idx,id in enumerate(data_dict['mt20id']):
        check_query = f"SELECT * FROM performance WHERE pf_id = %s"
        cur.execute(check_query,(id,))
        result = cur.fetchall()
        
        if result != []:
            print("중복값 존재. bye")

        else:
            name = data_dict['name'][idx]
            author = data_dict['author'][idx]
            creator = data_dict['creator'][idx]

            ex_query = "INSERT INTO performance(pf_id, pf_nm, author, creator) VALUES (%s,%s,%s,%s)"
            cur.execute(ex_query,(id,name,author,creator))
            conn.commit()
            # conn.close()
    

#공연별 상세 정보 수집 후 파일 저장
def get_pf_detail(ST_DT):

    config = configparser.ConfigParser()
    config.read('config/config.ini')
    SERVICE_KEY = config.get('KOPIS_KEYS', 'API_KEY')

    """
    db에서 쿼리로 공연 id 받아와서 아래 PF_ID_LIST로 선언
    """
    # 확인용 string
    new_file = ''

    PF_ID_LIST = []
    select_query = f'SELECT pf_id FROM performance WHERE created_at = "{ST_DT}"'
    cur.execute(select_query)
    PF_ID_LISTS = cur.fetchall()
    PF_ID_LIST = [x[0] for x in PF_ID_LISTS]

    for id in PF_ID_LIST:
        # PF_ID = "PF223258"
        tmp_path = "api/datas/kopis"
        file_name = f"KOPIS_showDetails_{id}.xml"
        xml_file_path = os.path.join(tmp_path, file_name)

        url = f"http://kopis.or.kr/openApi/restful/pblprfr/{id}?service={SERVICE_KEY}"
        request= Request(url)
        xml_data = urlopen(request).read()

        # XML 데이터 파싱
        root = ET.fromstring(xml_data)
        db_element = root.find('.//db')

        # 예매처 크롤링하여 정보 받아오기
        ticket_nm, ticket_href=get_ticket_page(id) 

        # tksites 태그 추가
        ticket_element = ET.SubElement(db_element, 'tksites')

        # 예매처 목록 추가
        for idx, nm in enumerate(ticket_nm):
            site_element= ET.SubElement(ticket_element, 'tksite')  
            site_element.set('href', ticket_href[idx])
            site_element.text = nm  

        # 수정된 XML 파일 저장
        tree = ET.ElementTree(root)
        tree.write(xml_file_path, encoding='utf-8')


        new_file += str(xml_file_path)


    return new_file