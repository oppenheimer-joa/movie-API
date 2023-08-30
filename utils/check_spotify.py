import os, re, datetime, subprocess
from lib.modules import *

#date_gte 기준으로 +6일 치 데이터 먼저 뽑고 id 리스트 만들고 리스트 갯수 세서 file 갯수와 같은지 확인
def spotify_file_check(now_date):

    # MySQL 연결
    conn = db_conn()

    cursor = conn.cursor()
    query = f"select * from movie_all where date_gte = '{now_date}'"
    
    cursor.execute(query)
    movie_cnt = len(cursor.fetchall())


    directory_path = "./datas/spotify"

    json_files_list= []

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            json_files_list.append(filename)

    json_file_cnt = len(json_files_list)

    if json_file_cnt == movie_cnt:
        conn.close()
        return "0"
    else:
        conn.close()
        return "1"
