import os, sys, json
from datetime import datetime, timedelta
from mysql import connector

# Date 파라미터 입력
# date_argv = sys.argv[1]
date_argv = "2023-08-21"

# Date 범위 지정
date_gte = datetime.strptime(date_argv, "%Y-%m-%d")
primary_release_date_gte = date_gte.strftime("%Y-%m-%d")
date_lte = date_gte + timedelta(days=6)
primary_release_date_lte = date_lte.strftime("%Y-%m-%d")
date_range = f"{primary_release_date_gte}_{primary_release_date_lte}"

# 파일 홈 디렉토리
# <수정 필요>
home_dir = "/Users/kimdohoon/git/hooniegit/TMDB-data-discover/datas/discoverMovie/date_range"

# 영화ID 정보 리스트 생성
list_merged = []

# json 파일의 영화ID 정보 출력 + 리스트에 추가
for filename in os.listdir(home_dir):
    if filename.endswith(".json"):
        file_path = f"{home_dir}/{filename}"
        print(file_path)
        with open (file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for result in data["results"]:
            id = result["id"]
            list_merged.append(id)

# database connection
conn = connector.connect(user="root",\
                        password="XXXX", \
                        host="XX.XX.XXX.XXX", \
                        database="XXXX", \
                        port="3306")
cursor = conn.cursor()

# database update
for movie_id in list_merged:
    # QUERY 로직 생성
    QUERY = f'''
        INSERT INTO XXXX(movie_id, date)
        VALEUS ({movie_id}, {primary_release_date_gte})
    '''
    cursor.execute(QUERY)
    conn.commit()