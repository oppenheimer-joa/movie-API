import requests, datetime, json, os, configparser
import pandas as pd

def get_daily_box_office(date:str):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    SERVICE_KEY = config.get('KOBIS_KEYS', 'API_KEY')

    service_url = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    }
    params = {
        "key": SERVICE_KEY,
        "targetDt": date
    }
    response = requests.get(url=service_url, headers=headers, params=params).json()
    """
    파일 write 코드입력 필
    """

def 