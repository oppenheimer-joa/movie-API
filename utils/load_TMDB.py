import sys, os, requests, json, configparser
from datetime import datetime, timedelta
import mysql.connector

# movie 리스트 가져오는 endPoint
def load_discoverMovie(date):

	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')

	# 파일 홈 디렉토리
	home_dir = "api/datas/TMDB/lists"

	# Date 파라미터 입력
	date_argv = date
	date_gte = datetime.strptime(date_argv, "%Y-%m-%d")
	date_lte = date_gte + timedelta(days=6)

	# Request 요청 파라미터
	include_adult = "true"
	include_video = "true"
	language = "ko-KR"
	primary_release_date_gte = date_gte.strftime("%Y-%m-%d")
	primary_release_date_lte = date_lte.strftime("%Y-%m-%d")

	# 페이지 제한 이내의 request 요청
	for page in range(1, 501):
		url = f"https://api.themoviedb.org/3/discover/movie?include_adult={include_adult}&include_video=true&language={language}&primary_release_date.gte={primary_release_date_gte}&primary_release_date.lte={primary_release_date_lte}&page={page}&sort_by=primary_release_date.desc"

		headers = {
	        "accept": "application/json",
	        "Authorization": f"Bearer {api_key}"
		}

		response = requests.get(url, headers=headers).json()
		if len(response["results"]) == 0: break

		date_range = f"{primary_release_date_gte}_{primary_release_date_lte}"

		json_path = f"{home_dir}/TMDB_{date_range}_{page}.json"
		with open(json_path, "w") as file:
			json.dump(response, file, indent=4, ensure_ascii=False)
		print(f"LOAD SUCCEED : {url}")


# movie credits를 가져오는 endPoint
def load_movieCredits(date) :

	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')
 
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
	cursor.execute(f"SELECT movie_id FROM movie WHERE created_at = {date}")
	rows = cursor.fetchall()

	for row in rows:
		movie_id = row[0]
		# 파일 홈 디렉토리
		# <수정 필요>
		home_dir = "api/datas/TMDB/credit"

		# 영화ID 파라미터 입력
		# movie_id = sys.argv[1]
		# movie_id = 1101609

		# request 요청 파라미터
		language = "ko-KR"

		# request 요청
		url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
		headers = {
			"accept": "application/json",
			"Authorization": f"Bearer {api_key}"
		}
		response = requests.get(url, headers=headers).json()

		# 파일 저장
		json_path = f"{home_dir}/TMDB_movieCredits_{movie_id}.json"
		with open(json_path, "w", encoding="utf-8") as file:
			json.dump(response, file, indent=4, ensure_ascii=False)
			print(f"LOAD SUCCEED : {url}")


# movie 상세정보를 가져오는 endPoint
def load_movieDetails(date) :

	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')
 	
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
	cursor.execute(f"SELECT movie_id FROM movie WHERE created_at = {date}")
	rows = cursor.fetchall()

	for row in rows:
		movie_id = row[0]
		base_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
	
		headers = {
    	    "Authorization": f"Bearer {api_key}",
    	    "accept": "application/json"
    	}
	
		response = requests.get(base_url, headers=headers)
		response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
		json_data = response.json()
		
		try:
			# 파일 저장
			dir = f"api/datas/TMDB/detail/{movie_id}.json"
			with open (dir, "w", encoding="utf-8") as file:
				json.dump(json_data, file, indent=4, ensure_ascii=False)
			return f'TMDB_movieDetails_{movie_id}.json : Data received'

		except Exception as e:
			return f'TMDB_movieDetails_{movie_id}.json : No Data {str(e)}'
		

# movie images를 가져오는 endPoint
def get_TMDB_movieImages(date):

	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')
 
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
	cursor.execute(f"SELECT movie_id FROM movie WHERE created_at = {date}")
	rows = cursor.fetchall()

	for row in rows:
		movie_id = row[0]
		base_url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
		headers = {
			"Authorization": f"Bearer {api_key}",
			"accept": "application/json"
		}

		response = requests.get(base_url, headers=headers)
		response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
		json_data = response.json()

		if all(not json_data[key] for key in ["backdrops", "logos", "posters"]):
			return f'TMDB_movieImages_{movie_id}.json : No Data'
		else:
			try:
				# 파일 저장
				dir = f"/api/datas/TMDB/images/TMDB_movieImages_{movie_id}.json"
				with open (dir, "w", encoding="utf-8") as file:
					json.dump(json_data, file, indent=4, ensure_ascii=False)
				return f'TMDB_movieImages_{movie_id}.json : Data received'
			except Exception as e:
				return f'TMDB_movieImages_{movie_id}.json : Error {str(e)}'


# similar movie 정보를 가져오는 endPoint
def get_TMDB_movieSimilar(date):

	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')

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
	cursor.execute(f"SELECT movie_id FROM movie WHERE created_at = {date}")
	rows = cursor.fetchall()

	for row in rows:
		movie_id = row[0]
		base_url = f"https://api.themoviedb.org/3/movie/{movie_id}/similar"
		headers = {
			"Authorization": f"Bearer {api_key}",
			"accept": "application/json"
		}

		response = requests.get(base_url, headers=headers)
		response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
		json_data = response.json()

		if not json_data['results']:
			return f'TMDB_movieSimilar_{movie_id}.json : No Data'
		else:
			try:
				# 파일 저장
				dir = f"api/datas/TMDB/similar/TMDB_movieSimilar_{movie_id}.json"
				with open (dir, "w", encoding="utf-8") as file:
					json.dump(json_data, file, indent=4, ensure_ascii=False)
				return f'TMDB_movieSimilar_{movie_id}.json : Data received'
			except Exception as e:
				return f'TMDB_movieSimilar_{movie_id}.json : Error {str(e)}'
		

# 영화 인물 정보를 가져오는 endpoint		
def get_TMDB_peopleDetail(date):

	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')

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
	cursor.execute(f"SELECT people_id FROM people WHERE created_at = {date}")
	rows = cursor.fetchall()

	for row in rows:
		people_id = row[0]
		base_url = f"https://api.themoviedb.org/3/person/{people_id}"
		headers = {
			"Authorization": f"Bearer {api_key}",
			"accept": "application/json"
		}

		response = requests.get(base_url, headers=headers)
		response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
		json_data = response.json()

		try:
			# 파일 저장
			dir = f"api/datas/TMDB/people_detail/TMDB_peopleDetails_{people_id}.json"
			with open (dir, "w", encoding="utf-8") as file:
				json.dump(json_data, file, indent=4, ensure_ascii=False)
			return f'TMDB_peopleDetails_{people_id}.json : Data received'
		except Exception as e:
			return f'TMDB_peopleDetails_{people_id}.json : No Data {str(e)}'
                


# 영화ID를 DB에 저장
def make_movieList(date_gte):

    # config parse
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

    # date range 설정
    date = datetime.strptime(date_gte, "%Y-%m-%d")
    date_lte = date + timedelta(days=6)
    date_lte = date_lte.strftime("%Y-%m-%d")

    # request parameter
    tmdb_key = config.get("TMDB", "API_KEY")
    include_adult = "true"
    include_video = "true"
    language = "ko-KR"

    # 페이지 제한 이내의 request 요청
    for page in range(1, 501):

        # request 요청
        url = f"https://api.themoviedb.org/3/discover/movie?include_adult={include_adult}&include_video=true&language={language}&primary_release_date.gte={date_gte}&primary_release_date.lte={date_lte}&page={page}&sort_by=primary_release_date.desc"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {tmdb_key}"
        }
        results = requests.get(url, headers=headers).json()["results"]
        if len(results) == 0: break

        # 각 result별 작업 수행
        for result in results:

            # 데이터 추출
            id = result["id"]
            original_title = result["original_title"]

            # 쿼리 생성
            QUERY = f"INSERT INTO movie(movie_id, movie_nm) VALUES (%s, %s)"
            values = (id, original_title)

            # 데이터 적재
            cursor.execute(QUERY, values)
            conn.commit()


# 사람ID를 DB에 저장
def make_peopleList(date_gte):

    # config parse
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

    # request parameter
    tmdb_key = config.get("TMDB", "API_KEY")

    # 쿼리 생성
    QUERY = f"""SELECT movie_id from movie
                WHERE created_at = '{date_gte}'"""
    
    # 데이터 추출
    cursor.execute(QUERY)
    rows = cursor.fetchall()

    # 중복 제거용 파라미터
    unique_ids = set()
    people_list = []
    
    # movie_id 만큼의 request 요청
    for row in rows:

        # movie_id 편집
        movie_id = row[0]

        # request 요청
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {tmdb_key}"
        }
        response = requests.get(url, headers=headers).json()

        # people 리스트 생성
        cast = response["cast"]
        crew = response["crew"]
        people = crew + cast

        # 중복 제거
        for item in people:
            id_value = item.get("id")
            if id_value not in unique_ids:
                people_list.append(item)
                unique_ids.add(id_value)
        

    # 각 result별 작업 수행
    for person in people_list:

        # 데이터 추출
        id = person["id"]
        original_name = person["original_name"]
        print(f"{id} & {original_name}")

        # 쿼리 생성
        QUERY = f"INSERT INTO people(people_id, people_nm) VALUES (%s, %s)"
        values = (id, original_name)

        # 데이터 적재
        cursor.execute(QUERY, values)
        conn.commit()