import os
from fastapi import APIRouter, Request
from utils.load_KOPIS import *
from utils.load_TMDB import *
from utils.load_spotify import *
import datetime

router = APIRouter()

#공연 세부 정보 수집
@router.get("/kopis/information")
async def get_pf_detail_routes():

    #DB에서 코드가 날라와야함
    PF_ID_LIST = ['PF223258', 'PF223038', 'PF222985', 'PF222956']
    return get_pf_detail(PF_ID_LIST)

#공연 코드 DB에 적재
@router.get("/kopis/perfomance-to-db")
async def get_mt20id_routes():

    # 날짜를 어디서 쏠지 정하지 않아 현재 api 서버 시간을 grep
    ST_DT = datetime.datetime.now()
    return get_mt20id(ST_DT)

#TMDB 영화코드 DB 적재
@router.get("/tmdb/discover-movie")
async def get_tmdb_discoverMovies_routes(nowDate:str):
    return load_discoverMovie(nowDate)

#TMDB 출연진 수집
@router.get("/tmdb/credits")
async def get_tdmb_credits_routes(movieCode:str):
    return load_movieCredits(movieCode)

#TMDB 영화 세부정보 수집
@router.get("/tmdb/movie-details")
async def get_tmdb_movie_details_routes(movieCode:str):
    return load_movieDetails(movieCode)

#TMDB 영화 이미지 및 스틸컷 수집
@router.get("/tmdb/images")
async def get_tmdb_movie_images_routes(movieCode:str):
    return get_TMDB_movieImages(movieCode)

#TMDB 비슷한 영화 케이터링 데이터 수집
@router.get("/tmdb/moive-similar")
async def get_tmdb_moive_similar_routes(movieCode:str):
    return get_TMDB_movieSimilar(movieCode)

#TMDB 출연진 및 배우 및 기타 인원 정보 수집
@router.get("/tmdb/people-details")
async def get_tmdb_people_details_routes(peopleCode:str):
    return get_TMDB_peopleDetail(peopleCode)

@router.get("/spotify/movie-ost")
async def get_spotify_ost_routes(movieCode:str):
    token = get_h_spotify_token()
    movieName = "엘리멘탈"
    return get_soundtrack(movieName, token)



