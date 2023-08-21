import sys, requests, json
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxMzllMGE3ZTBhZmRkNjg3ZDQ0Njc1NTVhNzA4NzIwNyIsInN1YiI6IjY0ZGMyY2M5Yjc3ZDRiMTE0MDE4YzAwMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.sjjmrmLiPAw6lbU9NSLvhQlaFYli3rfCSKI-9Rpai-s"

# 파일 홈 디렉토리
# <수정 필요>
home_dir = "/Users/kimdohoon/git/openheimer/movie-API/datas/movieCredits"

# 영화ID 파라미터 입력
# movie_id = sys.argv[1]
movie_id = 1101609

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