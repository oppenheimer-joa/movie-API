import os
from fastapi import APIRouter, Request
from utils.load_KOPIS import *
from utils.load_TMDB import *

router = APIRouter()

@router.get("/kopis/load")
async def get_pf_detail_routes():
    PF_ID_LIST = ['PF223258', 'PF223038', 'PF222985', 'PF222956']
    return get_pf_detail(PF_ID_LIST)

@router.get("/tmdb/discover-movie")
async def get_tmdb_discoverMovies_routes(nowDate:str):
    return load_discoverMovie(nowDate)
