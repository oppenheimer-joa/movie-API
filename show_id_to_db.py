from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import datetime

ST_DT = datetime.datetime.now()

def get_mt20id(start_date): # end_date는 Dag에서 start_date(execution_date가 되겠지요?)기준 timedelta로 +4주로 계산
    SERVICE_KEY= '975d079c508a44f6b03d6c08a40407de'
    # SERVICE_KET= "31280b49359d4d2f803e7be37702e8c7"
    CPAGE=1
    ROWS= '10'

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
    
get_mt20id(ST_DT)