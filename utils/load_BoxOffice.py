import requests, datetime, json, os, configparser
import mysql.connector

#date형식 YYYYmmdd
def get_daily_box_office(now_date, area_code):
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    SERVICE_KEY = config.get('KOBIS_KEYS', 'API_KEY')

    service_url = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    }
    params = {
        "key": SERVICE_KEY,
        "targetDt": date,
        "wideAreaCd": area_code
    }
    response = requests.get(url=service_url, headers=headers, params=params).json()

    data_path = "/api/datas/kobis"
    json_name = f"{now_date}_{area_code}_boxOffice.json"
    json_path = f"{data_path}/{json_name}"

    try:
        with open(json_path, "w") as file:
            json.dump(response, file, indent=4, ensure_ascii=False)
        return f"{json_name} load compelete!"
    except Exception as e:
        return f"{json_name} load failed!"

def update_movie_location_code():
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    SERVICE_KEY = config.get('KOBIS_KEYS', 'API_KEY')

    host = config.get('MYSQL', 'MYSQL_HOST')
    user = config.get('MYSQL', 'MYSQL_USER')
    password = config.get('MYSQL', 'MYSQL_PWD')
    database = config.get('MYSQL', 'MYSQL_DB')

    # MySQL 연결
    conn = mysql.connector.connect(host=host,
                                   user=user,
                                   password=password,
                                   database=database)
    cursor = conn.cursor()

    url = "http://kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.json"
    params = {
        "key" : SERVICE_KEY,
        "comCode" : "0105000000"
    }
    resp_data = requests.get(url=url, params=params).json()

    insert_query = "INSERT INTO codes (location_code, location_name) VALUES (%s, %s)"
    for data in resp_data['codes']:
        cursor.execute(insert_query, (data['fullCd'], data['korNm']))

    conn.close()