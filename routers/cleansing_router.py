import os, datetime
from fastapi import APIRouter, Request
from utils.cleansing import *

router = APIRouter()

@router.get("/cleansing/boxoffice")
async def cleanse_boxoffice_routes(now_date):
	return cleanse_daily_box_office(now_date)

@router.get("/cleansing/imdb")
async def cleanse_imdb_routes(event, year):
	return cleanse_awards(event, year)

@router.get("/cleansing/kopis")
async def cleanse_kopis_routes(ST_DT):
	return cleanse_pf_detail(ST_DT)

@router.get("/cleansing/spotify")
async def cleanse_spotify_routes():
	return cleanse_soundtrack()

@router.get("/cleansing/tmdb")
async def cleanse_tmdb_routes(category, date):
	return cleanse_tmdb(category, date)
