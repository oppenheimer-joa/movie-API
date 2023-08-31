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
	return blob_imdb(event,year)

# BoxOffice (KOBIS) 데이터 정합성 체크: 데이터가 받아진 디렉토리에서 파일 개수 체크
@router.get("/blob/boxoffice")
async def blob_boxoffice_routes(date:str):
	return blob_kobis(date)

# TMDB 데이터 정합성 체크
@router.get("/blob/tmdb")
async def blob_tmdb_routes(category:str, date:str):
	return blob_tmdb(category,date)

# KOPIS (공연) 데이터 정합성 체크
@router.get("/blob/kopis")
async def blob_kopis_routes(st_dt:str):
	return blob_kopis(st_dt)

# Spotify 데이터 정합성 체크
@router.get("/blob/spotify")
async def check_spotify_routes(year: int):
	return blob_spotify(year)