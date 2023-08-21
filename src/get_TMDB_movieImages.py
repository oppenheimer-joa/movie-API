import requests
import json
import sys
sys.path.append('/home/kjh/code/')
from API_key import api_key
from MySQL import config
import mysql.connector

def get_TMDB_movieImages(api_key, movieID):
    base_url = f"https://api.themoviedb.org/3/movie/{movieID}/images"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
#    params = {
#        "movie_id": movieID
#    }

    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
    json_data = response.json()
        
    if all(not json_data[key] for key in ["backdrops", "logos", "posters"]):
        return f'TMDB_movieImages_{movieID}.json : No Data'
    else:
        try:
            # 파일 저장
            dir = f"/home/kjh/code/SMS/movie-API/datas/movieImages/TMDB_movieImages_{movieID}.json"
            with open (dir, "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)
            return f'TMDB_movieImages_{movieID}.json : Data received'
        except Exception as e:
            return f'TMDB_movieImages_{movieID}.json : Error {str(e)}'


#def get_movieID(movieID_list_path):
#    with open(movieID_list_path, "r") as file:
#        content = file.read()
#        movieID_list = ast.literal_eval(content)
        
#movieID_list = [1149397, 1148207, 1124704, 1110836, 1105551, 1101609, 1096299, 1095454, 1093883, 1084806, 1083546, 1073304, 1068732, 1063814, 1059072, 1039006, 1037695, 1030334, 1029986, 997614]
#for movieID in movieID_list:
#    message = get_TMDB_movieImages(api_key, movieID)
#    print(message)
    
def DB_to_json(date_gte):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute(f"SELECT movieID FROM test WHERE date_gte = {date_gte}")
    rows = cursor.fetchall()

    for row in rows:
        movieID = row[0]
        message = get_TMDB_movieImages(api_key, movieID)
        print(message)