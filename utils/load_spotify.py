import json, requests, configparser, mysql.connector
from datetime import datetime


#spotify OST 정보는 DB에 밀어넣어진 데이터 기반 날짜로 가지고와서 리스트로 반환하거나 하면 될듯? 아니면 airflow 한테 맡겨도 되고ㅎㅎ

def get_h_spotify_token():

    config = configparser.ConfigParser()
    config.read('config/config.ini')

    client_id = config.get('SPOTIFY', 'client_id')
    client_sc = config.get('SPOTIFY', 'client_sc')

    # requests
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_sc}'.encode()
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()
 
    # return access token
    access_token = response['access_token']
    return access_token

#movie_id 를 DB에서 빨아온 movie_nm 으로 교체 후 진행
def get_soundtrack(movie_code, access_token):

    config = configparser.ConfigParser()
    config.read('config/config.ini')
 
    # MySQL 연결정보
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
    query = f"select * from movie_all where movie_id = '{movie_code}'"

    cursor.execute(query)
    raw_data = cursor.fetchall()

    movie_year = datetime.strftime(raw_data[0][1], '%Y')
    movie_name = raw_data[0][2]

    query = f"{movie_name}%{movie_year}year"

    # requests
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'q' : query,
        'type': 'album',
        'limit' : "3"
    }
    response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers).json()

    # file save
    data_path = "/api/datas/spotify"
    #data_path = "/Users/jesse/Documents/sms/API/datas/spotify"
    json_name = f"spotify_{movie_year}_{movie_code}_.json"
    json_path = f"{data_path}/{json_name}"

    try:
        with open(json_path, "w") as file:
            json.dump(response, file, indent=4, ensure_ascii=False)
        return f"{json_name} load compelete!"
    except Exception as e:
        return f"{json_name} load failed!"

