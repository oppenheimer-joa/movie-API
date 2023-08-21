import requests
import json
import ast
import sys
sys.path.append('/home/kjh/code/')
from API_key import api_key
from MySQL import config
import mysql.connector

def get_TMDB_peopleDetail(api_key, peopleID):
    base_url = f"https://api.themoviedb.org/3/person/{peopleID}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }

    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
    json_data = response.json()
        
    try:
        # 파일 저장
        dir = f"/home/kjh/code/SMS/movie-API/datas/peopleDetails/TMDB_peopleDetails_{peopleID}.json"
        with open (dir, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        return f'TMDB_peopleDetails_{peopleID}.json : Data received'
    except Exception as e:
        return f'TMDB_peopleDetails_{peopleID}.json : No Data {str(e)}'    
        

#def get_movieID(peopleID_list_path):
#    with open(peopleID_list_path, "r") as file:
#        content = file.read()
#        peopleID_list = ast.literal_eval(content)

#peopleID_list = [3578734, 2875508, 2538610, 2115929, 3967549, 3753413, 3103691, 2744392, 1969995, 1698009, 2363030, 2755969, 3967550, 3967551, 3966921, 3967552, 3967553, 3967554, 3968525, 3968526, 3967558, 3578735, 3991943, 3966949, 1773700, 222497, 222497, 222497, 1564935, 1922605, 2755969, 3206228, 3371937, 3578734, 3578734, 3653591, 3966921, 3966921, 3966944, 3966946, 3966946, 3967554, 3967554, 3967556, 3967557, 3967558, 3968521, 3968523, 3968524, 3986579, 3995891]
#for peopleID in peopleID_list:
#    message = get_TMDB_peopleDetail(api_key, peopleID)
#    print(message)
    
def DB_to_json(date_gte):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"SELECT peopleID FROM test WHERE date_gte = {date_gte}")
    rows = cursor.fetchall()

    for row in rows:
        peopleID = row[0]
        message = get_TMDB_peopleDetail(api_key, peopleID)
        print(message)