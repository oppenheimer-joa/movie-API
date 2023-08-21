import os, sys
from datetime import datetime, timedelta

# 파일 홈 디렉토리
# <수정 필요>
home_dir = "/Users/kimdohoon/git/openheimer/movie-API/datas/discover/movie"

# 날짜 파라미터 입력
# date_argv = sys.argv[1]
date_argv = "2023-08-21"
date_gte = datetime.strptime(date_argv, "%Y-%m-%d")
date_lte = date_gte + timedelta(days=6)
primary_release_date_gte = date_gte.strftime("%Y-%m-%d")
primary_release_date_lte = date_lte.strftime("%Y-%m-%d")


# 폴더 디렉토리 생성
os.mkdir(f"{home_dir}/{primary_release_date_gte}_{primary_release_date_lte}")