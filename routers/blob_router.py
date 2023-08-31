import os, datetime
from fastapi import APIRouter, Request
from utils.blob_IMDB import *
from utils.blob_BoxOffice import *
from utils.blob_KOPIS import *
from utils.blob_TMDB import *
from utils.blob_spotify import *

router = APIRouter()

# IMDB 데이터 정합성 체크: 데이터가 받아진 디렉토리에서 데이터 파일 크기 체크
@router.get("/blob/imdb")
async def blob_imdb_routes(event:str, year:int):
	"""
    <h3> [IMDB] IMDB 수집된 데이터 정합성 체크 </h3>

    IMDB Crawler로 수집된 영화제 시상목록 데이터가 문제없이 서버에 저장되었는지 확인합니다.
    해당 로직은 파일크기를 기반으로 endPoint별 데이터의 이상점을 체크합니다.

    <br><br>

    만약, 데이터의 정합성에 문제가 발생한다면, 1을 반환하며, 문제가 없을시 0을 반환합니다.

    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/check/imdb?event={event_name}&year=2022'
    ```
    """
	return blob_imdb(event,year)

# BoxOffice (KOBIS) 데이터 정합성 체크: 데이터가 받아진 디렉토리에서 파일 개수 체크
@router.get("/blob/boxoffice")
async def blob_boxoffice_routes(date:str):
	"""
    <h3> [KOBIS] 국내 Box-Office 관련 수집된 데이터 정합성 체크 </h3>

    KOBIS API 로 수집된 국내 박스오피스 순위 및 기타 정보 데이터가 문제없이 서버에 저장되었는지 확인합니다.
    해당 로직은 지역별 코드별로 데이터를 저장한 숫자를 기반으로 데이터의 무결정을 체크합니다.

    <br><br>

    만약, 데이터의 정합성에 문제가 발생한다면, 1을 반환하며, 문제가 없을시 0을 반환합니다.

    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/check/boxoffice'
    ```
    """
	return blob_kobis(date)

# TMDB 데이터 정합성 체크
@router.get("/blob/tmdb")
async def blob_tmdb_routes(category:str, date:str):
	"""
    <h3> [TMDB] TMDB API 수집 데이터 정합성 체크 </h3>

    TMDB API 로 수집된 6개의 TMDB endPoint 에서 적재된 데이터가 문제없이 서버에 저장되었는지 확인합니다.
    해당 로직은 당일 처리해야할 영화 수를 xcom, 6개의 각기 다른 endPoint를 category, 해당 날짜를 date에 넣어
    날짜별 추가된 movieCode를 기반으로 무결성을 체크합니다.

    <br><br>

    category에 들어갈 Variable은 아래와 같습니다.
    - discoverMovie
    - movieCredits
    - movieDetails
    - movieImages
    - movieSimilar
    - peopleDetail	

    만약, 데이터의 정합성에 문제가 발생한다면, 1을 반환하며, 문제가 없을시 0을 반환합니다.

    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/check/tmdb?xcom={당일_DB_cnt}&category={TMDB_API_종류}&date=2023-01-01'
    ```
    """
	return blob_tmdb(category,date)

# KOPIS (공연) 데이터 정합성 체크
@router.get("/blob/kopis")
async def blob_kopis_routes(st_dt:str):
	"""
    <h3> [KOPIS] KOPIS API 공연 데이터 정합성 체크 </h3>

    KOPIS API 로 수집된 공연 상세 정보 데이터가 문제없이 서버에 저장되었는지 확인합니다.
    해당 로직은 DB내 업데이트 된 공연ID 숫자를 기반으로 데이터의 무결정을 체크합니다.

    <br><br>

    만약, 데이터의 정합성에 문제가 발생한다면, 1을 반환하며, 문제가 없을시 0을 반환합니다.

    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/check/kopis?st_dt=2023-06-01&db_cnt={db_cnt}'
    ```
    """
	return blob_kopis(st_dt)

# Spotify 데이터 정합성 체크
@router.get("/blob/spotify")
async def check_spotify_routes(year: int):
	"""
    <h3> [Spotify] Spotify API 영화 OST 정보 정합성 체크 </h3>

    Spotify API 로 수집된 업데이트 된 영화의 OST 데이터가 문제없이 서버에 저장되었는지 확인합니다.
    해당 로직은 DB내 업데이트 된 영화ID 수를 기반으로 데이터의 무결정을 체크합니다.

    <br>

    만약, 데이터의 정합성에 문제가 발생한다면, 1을 반환하며, 문제가 없을시 0을 반환합니다.

    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/check/spotify?now_date={now_date}'
    ```
    now_date 에는 Base_DB 의 date_gte 기반으로 체크되며, db_gte는 일주일기준 매주 금요일로 로드되어집니다.
    """
	return blob_spotify(year)