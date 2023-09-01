from urllib.request import urlopen, Request
import os, datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from lib.modules import *

# 티켓 페이지 크롤러 내장 함수
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


# date 기준 4주 동안 공연 기간이 속하고 & DB에 없는 데이터 insert 함수
def get_mt20id(ST_DT): # end_date는 Dag에서 start_date(execution_date기준 timedelta +4주로 계산
    # db connection
    conn = db_conn()
    cur = conn.cursor()
    SERVICE_KEY = get_config('KOPIS_KEYS', 'API_KEY')
    
    CPAGE=1
    ROWS= '100' 
    db_insert_cnt = 0

    ST_DT = datetime.datetime.strptime(ST_DT, '%Y-%m-%d')
    END_DT= (ST_DT + datetime.timedelta(weeks=4)).strftime("%Y%m%d")
    ST_DT_2= ST_DT.strftime("%Y%m%d")
    ST_DT = ST_DT.strftime("%Y-%m-%d")

    url = f'http://www.kopis.or.kr/openApi/restful/pblprfr?service={SERVICE_KEY}&stdate={ST_DT_2}&eddate={END_DT}&cpage={CPAGE}&rows={ROWS}'

    result = urlopen(url)
    data = bs(result, 'lxml-xml')
    db = data.find_all('db')
    
    id, nm = [], []
    
    for pf in db :
        pf_id = pf.find('mt20id').text
        pf_nm = pf.find('prfnm').text
        id.append(pf_id)
        nm.append(pf_nm)

    data_dict={}
    data_dict['mt20id']=id
    data_dict['name']=nm

    for idx,id in enumerate(data_dict['mt20id']):
        check_query = f"SELECT * FROM performance WHERE pf_id = %s"
        cur.execute(check_query,(id,))
        result = cur.fetchall()
        
        if result != []:
            pass

        else:
            name = data_dict['name'][idx]
            ex_query = "INSERT INTO performance(created_at, pf_id, pf_nm) VALUES (%s,%s,%s)"
            cur.execute(ex_query,(ST_DT,id,name))
            conn.commit()
            db_insert_cnt += 1 

    conn.close()
    return db_insert_cnt
    

# 공연별 상세 정보 수집 후 xml 파일 저장
def get_pf_detail(ST_DT):
    # db connection
    conn = db_conn()
    cur = conn.cursor()
    SERVICE_KEY = get_config('KOPIS_KEYS', 'API_KEY')

    select_query = f'SELECT pf_id FROM performance WHERE created_at = "{ST_DT}"'
    cur.execute(select_query)
    PF_ID_LISTS = cur.fetchall()
    PF_ID_LIST = [x[0] for x in PF_ID_LISTS]

    return_string=[]

    for id in PF_ID_LIST:
 
        tmp_path = "./datas/kopis"
        file_name = f"KOPIS_showDetails_{ST_DT}_{id}.xml"
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

        try :
            tree.write(xml_file_path, encoding='utf-8')
            return_string.append(f"{str(file_name)} load compelete!")
        except:
            return_string.append(f"{str(file_name)} load failed!")

    conn.close()
    return  return_string
