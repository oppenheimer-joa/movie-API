import os
from fastapi import APIRouter, Request

#from utils.scout_modules import *
from utils.test_func import *

router = APIRouter()

@router.get("/test/")
async def test():
    return 11111