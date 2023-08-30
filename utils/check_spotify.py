import os, re, datetime, subprocess, mysql.connector, configparser

#date_gte 기준으로 +6일 치 데이터 먼저 뽑고 id 리스트 만들고 리스트 갯수 세서 file 갯수와 같은지 확인
def spotify_file_check(now_date):

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
        return "0"
    else:
        return "1"
