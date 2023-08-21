from urllib.request import urlopen, Request
import os
import configparser

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