
# make_accessToken(1)
# make_accessToken(2)
# make_accessToken(3)
# make_accessToken(4)
# make_accessToken(5)
def make_accessToken(cnt):
    from configparser import ConfigParser
    import requests

    parser = ConfigParser()
    parser.read('/home/hooniegit/config/config.ini')
    client_id = parser.get("SPOTIFY", f"client_id_{cnt}")
    client_sc = parser.get("SPOTIFY", f"client_sc_{cnt}")

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_sc}'.encode()
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()
    access_token = response['access_token']

    return access_token

def make_movieList(conn, start_date, end_date):
    cursor = conn.cursor()

    QUERY = f"SELECT * from movie where date_gte>'{start_date}' and date_gte<'{end_date}' "
    cursor.execute(QUERY)
    movie_list = cursor.fetchall()
    conn.close()
    return movie_list

def load_json(token, movie_id, movie_name, date_gte):
    from datetime import datetime
    import requests
    import json

    year = date_gte.strftime("%Y")

    query = f"{movie_name}"
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        'q' : query,
        'type': 'album',
        'limit' : "3"
    }
    response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        data_path = f"/home/hooniegit/datas/spotify/{year}"
        json_name = f"spotify_{movie_id}_{year}.json"
        json_path = f"{data_path}/{json_name}"

        try:
            with open(json_path, "w") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(e)
    else:
        print("Error Appeared.")


def thread_single(token, movie_list):
    import time
    print(f"start thread >>>>>>")
    for movie in movie_list:
        movie_id = movie[0]
        movie_name = movie[1]
        date_gte = movie[2]
        load_json(token, movie_id, movie_name, date_gte)
        time.sleep(1)

    print(f"<<<<<< end thread")
    with open(f"/home/hooniegit/DONE/spotify/{date_gte}", "w") as file:
        pass