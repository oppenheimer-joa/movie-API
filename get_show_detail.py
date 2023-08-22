
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
import xml.etree.ElementTree as ET
import os 


# 예매처 크롤링 함수
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

#공연별 상세 정보 수집 후 파일 저장
def get_pf_detail(PF_ID_LIST):

    SERVICE_KEY= '975d079c508a44f6b03d6c08a40407de'

    """
    db에서 쿼리로 공연 id 받아와서 아래 PF_ID_LIST로 선언
    """

    for id in PF_ID_LIST:
        # PF_ID = "PF223258"
        tmp_path = "/home/yoda/sms/extract/kopis"
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

# 테스트
# PF_ID_LISt=['PF223258', 'PF223038']
# get_pf_detail(PF_ID_LISt)