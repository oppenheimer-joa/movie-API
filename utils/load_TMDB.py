import sys, requests, json, configparser
from datetime import datetime, timedelta

# movie 리스트 가져오는 endPoint
def load_discoverMovie(now_date):

	config = configparser.ConfigParser()
	config.read('config/config.ini')
	api_key = config.get('TMDB', 'API_KEY')

	# 파일 홈 디렉토리
	home_dir = "api/datas"

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