import os
from fastapi import APIRouter, Request
from utils.load_KOPIS import *
from utils.load_TMDB import *
import datetime

router = APIRouter()

#공연 세부 정보 수집
@router.get("/kopis/information")
async def get_pf_detail_routes():

    #DB에서 코드가 날라와야함
    ST_DT = datetime.datetime.now().strftime('%Y-%m-%d')
    # PF_ID_LIST = ['PF223258', 'PF223038', 'PF222985', 'PF222956']
    return get_pf_detail(ST_DT)

#공연 코드 DB에 적재
@router.get("/kopis/perfomance-to-db")
async def get_mt20id_routes():

    # 날짜를 어디서 쏠지 정하지 않아 현재 api 서버 시간을 grep
    ST_DT = datetime.datetime.now()
    return get_mt20id(ST_DT)

#TMDB 영화코드 DB 적재
@router.get("/tmdb/discover-movie")
async def get_tmdb_discoverMovies_routes(date:str):
    return load_discoverMovie(date)

#TMDB 출연진 수집
@router.get("/tmdb/movie-credits")
async def get_tdmb_credits_routes(date:str):
    return load_movieCredits(date)

#TMDB 영화 세부정보 수집
@router.get("/tmdb/movie-details")
async def get_tmdb_movie_details_routes(date:str):
    return load_movieDetails(date)

#TMDB 영화 이미지 및 스틸컷 수집
@router.get("/tmdb/movie-images")
async def get_tmdb_movie_images_routes(date:str):
    return get_TMDB_movieImages(date)

#TMDB 비슷한 영화 케이터링 데이터 수집
@router.get("/tmdb/movie-similar")
async def get_tmdb_movie_similar_routes(date:str):
    return get_TMDB_movieSimilar(date)

#TMDB 출연진 및 배우 및 기타 인원 정보 수집
@router.get("/tmdb/people-details")
async def get_tmdb_people_details_routes(date:str):
    return get_TMDB_peopleDetail(date)

#TMDB 영화ID 데이터 DB 적재
@router.get("/tmdb/mysql-movie")
async def insert_movie_lists(date:str):
    return make_movieList(date)

#TMDB 인물ID 데이터 DB 적재
@router.get("/tmdb/mysql-people")
async def insert_people_lists(date:str):
    return make_peopleList(date)