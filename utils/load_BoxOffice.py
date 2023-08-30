import requests, datetime, json, os
from lib.modules import *

#date형식 YYYYmmdd
def get_daily_box_office(now_date, area_code):

    SERVICE_KEY = get_config('KOBIS_KEYS', 'API_KEY')

    service_url = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"
    headers = {
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15"
    }
    params = {
        "key": SERVICE_KEY,
        "targetDt": now_date,
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

    SERVICE_KEY = get_config('KOBIS_KEYS', 'API_KEY')


    # MySQL 연결
    conn = db_conn(charset=False)
    cursor = conn.cursor()

    url = "http://kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.json"
    params = {
        "key" : SERVICE_KEY,
        "comCode" : "0105000000"
    }
    resp_data = requests.get(url=url, params=params).json()

    insert_query = "INSERT INTO movie_location (location_code, location_name) VALUES (%s, %s)"

    try : 
        for data in resp_data['codes']:
            values = (data['fullCd'], data['korNm'])
            cursor.execute(insert_query, values)
            conn.commit()
        conn.close()
        return f"{insert_query} complete!"
        
    except Exception as e:
        conn.close()
        return f"{insert_query} failed!"
