import sys, json
from mysql import connector

# 파일 홈 디렉토리
# <수정 필요>
home_dir = "/Users/kimdohoon/git/hooniegit/TMDB-data-discover/datas/moviesCredits"

# 영화ID 파라미터 입력
# movie_id = sys.argv[1]
movie_id = 1101609

# 인물ID 정보 리스트 생성
list_merged = []

# json 파일의 영화ID 정보 출력 + 리스트에 추가
file_path = f"{home_dir}/TMDB_moviesCredits_{movie_id}.json"
with open (file_path, "r", encoding="utf-8") as file:
    data = json.load(file)
for result in data["cast"]:
    id = result["id"]
    list_merged.append(id)
for result in data["crew"]:
    id = result["id"]
    list_merged.append(id)

# database connection
conn = connector.connect(user="root",\
                        password="XXXX", \
                        host="XX.XX.XXX.XXX", \
                        database="XXXX", \
                        port="3306")
cursor = conn.cursor()

date = None
# database update
for people_id in list_merged:
    # QUERY 로직 생성
    QUERY = f'''
        INSERT INTO XXXX(people_id, date)
        VALEUS ({people_id}, {date})
    '''
    cursor.execute(QUERY)
    conn.commit()