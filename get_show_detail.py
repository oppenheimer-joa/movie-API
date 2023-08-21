
from urllib.request import urlopen, Request
import os 


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
        response_body = urlopen(request).read()

        with open(xml_file_path, "wb") as file:
            file.write(response_body)
