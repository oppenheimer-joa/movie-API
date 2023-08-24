import requests, datetime, json, os, configparser

def update_movie_location_code():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    SERVICE_KEY = config.get('KOBIS_KEYS', 'API_KEY')

    url = "http://kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.json?key=f5eef3421c602c6cb7ea224104795888&comCode=0105000000"
    params = {
        "key" : SERVICE_KEY,
        "comCode" : "0105000000"
    }