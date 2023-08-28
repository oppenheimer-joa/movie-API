import os, datetime
from fastapi import APIRouter, Request
from utils.check_IMDB import *
from utils.check_BoxOffice import *

router = APIRouter()

# IMDB 데이터 정합성 체크: 데이터가 받아진 디렉토리에서 데이터 파일 크기 체크
@router.get("/check/imdb/"):
async def check_imdb_routes(event:str, year:int):
	return imdb_file_check(event,year)

# BoxOffice (Kobis) 데이터 정합성 체크: 데이터가 받아진 디렉토리에서 파일 개수 체크
@router.get("/check/boxoffice/")
async def check_boxoffice_routes()
	return BoxOffice_file_check()