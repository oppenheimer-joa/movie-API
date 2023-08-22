import sys, requests, json, configparser
from datetime import datetime, timedelta


# movie 리스트 가져오는 endPoint
def load_discoverMovie(now_date):

	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')

	# 파일 홈 디렉토리
	home_dir = "api/datas/discover"

	# Date 파라미터 입력
	date_argv = now_date
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
def load_movieCredits(movie_id) :
        
	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')

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
def load_movieDetails(movieID) :
    
	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')
    
    base_url = f"https://api.themoviedb.org/3/movie/{movieID}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
    json_data = response.json()

    try:
        # 파일 저장
        dir = f"api/datas/TMDB/detail/{movieID}.json"
        with open (dir, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        return f'TMDB_movieDetails_{movieID}.json : Data received'
    except Exception as e:
        return f'TMDB_movieDetails_{movieID}.json : No Data {str(e)}'
        

# movie images를 가져오는 endPoint
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
            dir = f"/api/datas/TMDB/images/TMDB_movieImages_{movieID}.json"
            with open (dir, "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)
            return f'TMDB_movieImages_{movieID}.json : Data received'
        except Exception as e:
            return f'TMDB_movieImages_{movieID}.json : Error {str(e)}'


# similar movie 정보를 가져오는 endPoint
def get_TMDB_movieSimilar(api_key, movieID):
    base_url = f"https://api.themoviedb.org/3/movie/{movieID}/similar"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
    json_data = response.json()
        
    if not json_data['results']:
        return f'TMDB_movieSimilar_{movieID}.json : No Data'
    else:
        try:
            # 파일 저장
            dir = f"api/datas/TMDB/similar/TMDB_movieSimilar_{movieID}.json"
            with open (dir, "w", encoding="utf-8") as file:
                json.dump(json_data, file, indent=4, ensure_ascii=False)
            return f'TMDB_movieSimilar_{movieID}.json : Data received'
        except Exception as e:
            return f'TMDB_movieSimilar_{movieID}.json : Error {str(e)}'
        


# 영화 인물 정보를 가져오는 endpoint		
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
        dir = f"api/datas/TMDB/people_detail/TMDB_peopleDetails_{peopleID}.json"
        with open (dir, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        return f'TMDB_peopleDetails_{peopleID}.json : Data received'
    except Exception as e:
        return f'TMDB_peopleDetails_{peopleID}.json : No Data {str(e)}'