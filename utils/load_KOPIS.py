from urllib.request import urlopen, Request
import os
import configparser
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import datetime
from mysql import connector


ST_DT = datetime.datetime.now()

def get_mt20id(start_date): # end_date는 Dag에서 start_date(execution_date가 되겠지요?)기준 timedelta로 +4주로 계산

    config = configparser.ConfigParser()
    config.read('config/config.ini')
    SERVICE_KEY = config.get('KOPIS_KEYS', 'API_KEY')
    conn = connector.connect(**config) 

    CPAGE=1
    ROWS= '10'

    end_date= (start_date + datetime.timedelta(weeks=4)).strftime("%Y%m%d")
    start_date= start_date.strftime("%Y%m%d")
    print(start_date,end_date)

    url = f'http://www.kopis.or.kr/openApi/restful/prfper?service={SERVICE_KEY}&stdate={start_date}&eddate={end_date}&cpage={CPAGE}&rows={ROWS}'
    result = urlopen(url)
    data = bs(result, 'lxml-xml')
    pf_id = data.find_all('mt20id')
    pf_nm = data.find_all('prfnm')
    pf_author = data.find_all('author')
    pf_creator = data.find_all('creator')

    data_dict={}

    data_dict['mt20id']=[mt20id.text for mt20id in pf_id]
    data_dict['name']=[nm.text for nm in pf_nm]
    data_dict['author']=[author.text for author in pf_author]
    data_dict['creator']=[creator.text for creator in pf_creator]
    
    # print(data_dict)

    for idx,id in enumerate(data_dict['mt20id']):
        check_query = f"select * from 테이블명 where mt20id = %s"
        conn.excute(check_query,(id))
        result = conn.fetchall()
        
        if result != []:
            print("중복값 존재. bye")

        else:
            name = data_dict['name'][idx]
            author = data_dict['author'][idx]
            creator = data_dict['creator'][idx]

            ex_query = "insert into 테이블명(mt20id,name,author,creator) values (%s,%s,%s,%s)"
            conn.execute(ex_query,(id,name,author,creator))
            conn.close()
    

def get_pf_detail(PF_ID_LIST):

    """
    db에서 쿼리로 공연 id 받아와서 아래 PF_ID_LIST로 선언
    """

    config = configparser.ConfigParser()
    config.read('config/config.ini')
    SERVICE_KEY = config.get('KOPIS_KEYS', 'API_KEY')

    for id in PF_ID_LIST:
        PF_ID = "PF223258"
        tmp_path = "/api/datas/"
        file_name = f"KOPIS_showDetails_{id}.xml"
        xml_file_path = os.path.join(tmp_path, file_name)

        url = f"http://kopis.or.kr/openApi/restful/pblprfr/{PF_ID}?service={SERVICE_KEY}"
        request= Request(url)
        response_body = urlopen(request).read()

        with open(xml_file_path, "wb") as file:
            file.write(response_body)


        return f"{id} DONE \n {response_body}"