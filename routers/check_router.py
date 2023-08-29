import os, datetime
from fastapi import APIRouter, Request
#from utils.check_IMDB import *
#from utils.check_BoxOffice import *
#from utils.check_KOPIS import *
from utils.check_TMDB import *
#from utils.check_spotify import *

router = APIRouter()

## IMDB 데이터 정합성 체크: 데이터가 받아진 디렉토리에서 데이터 파일 크기 체크
#@router.get("/check/imdb/")
#async def check_imdb_routes(event:str, year:int):
#	return imdb_file_check(event,year)

## BoxOffice (KOIBS) 데이터 정합성 체크: 데이터가 받아진 디렉토리에서 파일 개수 체크
#@router.get("/check/boxoffice/")
#async def check_boxoffice_routes():
#	return BoxOffice_file_check()

# TMDB 데이터 정합성 체크
@router.get("/check/tmdb/")
async def check_tmdb_routes(xcom:int, category:str, date:str):
	return TMDB_file_check(xcom, category,date)

## KOPIS (공연) 데이터 정합성 체크
#@router.get("/check/kopis/")
#async def check_kopis_routes(st_dt:str, db_cnt:int):
#	return kopis_file_check(st_dt, db_cnt)

## Spotify 데이터 정합성 체크
#@router.get("/check/spotify")
#async def check_spotify_routes(now_date: str):
#	return spotify_file_check(now_date)