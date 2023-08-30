import os
from fastapi import APIRouter, Request
from utils.load_KOPIS import *
from utils.load_TMDB import *
from utils.load_spotify import *
from utils.load_IMDbAwards import *
from utils.load_BoxOffice import *
import datetime

router = APIRouter()

#공연 세부 정보 수집
@router.get("/kopis/information")
async def get_pf_detail_routes(date:str):
    """
    <h3> [KOPIS]공연 정보 적재 </h3>

    DB의 공연 코드를 기반으로 해당 공연의 세부 정보를 수집하여 API 서버 내 directory ~/.datas/kopis/ 에 저장합니다.
    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Week <br>
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/kopis/information?date=2023-01-01'
    ```
    """
    return get_pf_detail(date)

#공연 코드 DB에 적재
@router.get("/kopis/performance-to-db")
async def get_mt20id_routes(date:str):
    """
    <h3> [KOPIS] 공연 기본 정보 DB 적재 </h3>

    endPoint `/kopis/information?date={now_date}` 에 수집에 사용되는 기본 공연 코드를 Base_DB 에 중복값 제외 후 update 합니다.

    **Update Frequency** : 1 Week <br>
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/kopis/performance-to-db?date=2023-01-01'
    ```
    """
    return get_mt20id(date)

#TMDB 영화코드 DB 적재
@router.get("/tmdb/discover-movie")
async def get_tmdb_discoverMovies_routes(date:str):
    """
    <h3> [TMDB]영화 정보 적재 [23.08.30 기준 DB 아카이빙에 사용예정] </h3>

    모든 데이터를 적재 하기 위해 저장되는 DB의 문제가 생길 시 아카이빙하는 RAW_FILE을 ~/.datas/TMDB/discover 에 저장합니다.
    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Week [Friday 15:00 KST] <br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/tmdb/discover-movie?date=2023-01-01'
    ```
    """
    return load_discoverMovie(date)

#TMDB 출연진 수집
@router.get("/tmdb/movie-credits")
async def get_tdmb_credits_routes(date:str):
    """
    <h3> [TMDB]영화 제작 모든 관계자 정보 수집 [성인 영화 관계인물 제외] </h3>

    기존에 적재한 영화코드를 기반으로 영화 제작 관계자 데이터를 ~/.datas/TMDB/credit 에 저장합니다. 
    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Week <br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/tmdb/movie-credits?date=2023-01-01'
    ```
    """
    return load_movieCredits(date)

#TMDB 영화 세부정보 수집
@router.get("/tmdb/movie-details")
async def get_tmdb_movie_details_routes(date:str):
    """
    <h3> [TMDB]영화 상세 정보 </h3>

    기존에 적재한 영화코드를 기반으로 실제 영화에 대한 상세정보 데이터를 ~/.datas/TMDB/detail 에 저장합니다. 
    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Week <br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/tmdb/movie-details?date=2023-01-01'
    ```
    """
    return load_movieDetails(date)

#TMDB 영화 이미지 및 스틸컷 수집
@router.get("/tmdb/movie-images")
async def get_tmdb_movie_images_routes(date:str):
    """
    <h3> [TMDB] 영화 이미지 및 스틸컷 URL 수집 </h3>

    기존에 적재한 영화코드를 기반으로 영화 제작 관계자 데이터를 ~/.datas/TMDB/images 에 저장합니다. 
    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Week <br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/tmdb/movie-images?date=2023-01-01'
    ```
    """
    return get_TMDB_movieImages(date)

#TMDB 비슷한 영화 케이터링 데이터 수집
@router.get("/tmdb/movie-similar")
async def get_tmdb_movie_similar_routes(date:str):
    """
    <h3> [TMDB]비슷한 카테고리 영화 정보 수집 </h3>

    기존에 적재한 영화코드를 기반으로 영화 제작 관계자 데이터를 ~/.datas/TMDB/similar 에 저장합니다. 
    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Week <br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/tmdb/movie-similar?date=2023-01-01'
    ```
    """
    return get_TMDB_movieSimilar(date)

#TMDB 출연진 및 배우 및 기타 인원 정보 수집
@router.get("/tmdb/people-details")
async def get_tmdb_people_details_routes(date:str):
    """
    <h3> [TMDB]영화 제작 모든 관계자 상세 정보 수집 [성인 영화 관계인물 제외] </h3>

    기존에 적재한 영화코드를 기반으로 영화 제작 관계자 데이터를 ~/.datas/TMDB/people_detail 에 저장합니다.
    endPoint `/tmdb/movie-credits`와 join 하여 df를 생성할 수 있습니다. 
    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Week <br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/tmdb/people-details?date=2023-01-01'
    ```
    """
    return get_TMDB_peopleDetail(date)

#TMDB 영화ID 데이터 DB 적재
@router.get("/tmdb/mysql-movie")
async def insert_movie_lists(date:str):
    """
    <h3> [TMDB] TMDB 관련 json 수집을 위한 movieCode DB 적재 </h3>

    모든 TMDB json file 수집에 사용되는 기본 영화 코드를 Base_DB 에 중복값 제외 후 update 합니다.

    **Update Frequency** : 1 Week [Friday] 15:00 KST<br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/tmdb/mysql-movie?date=2023-01-01'
    ```
    """
    return make_movieList(date)

#TMDB 인물ID 데이터 DB 적재
@router.get("/tmdb/mysql-people")
async def insert_people_lists(date:str):
    """
    <h3> [TMDB] TMDB 관련 json 수집을 위한 peopleCode DB 적재 </h3>

    모든 TMDB json file 수집에 사용되는 기본 영화 관계자 Code 를 Base_DB 에 중복값 제외 후 update 합니다.

    **Update Frequency** : 1 Week [Friday] 15:00 KST<br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/tmdb/mysql-people?date=2023-01-01'
    ```
    """
    return make_peopleList(date)

# spotify 영화 OST 수집
@router.get("/spotify/movie-ost")
async def get_spotify_ost_routes(movieCode:str):
    """
    <h3> [Spotify] 영화 OST 관련 정보 수집 [성인 영화 OST 제외] </h3>

    기존에 적재한 영화코드를 전처리하여 Spotify API 를 통해 ~/.datas/spotify/ 에 저장합니다.
    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Week <br> 
    **Recommand call** : 1 call per Week<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/spotify/movie-ost?movieCode={DB_movieCode}'
    ```
    """
    token = get_h_spotify_token()
    return get_soundtrack(movieCode, token)

#IMDb 영화제(Academy, Cannes, Venice, Busan) 수상내역 크롤링
@router.get("/imdb/award")
async def get_imdb_awards(event:str, year:int):
    """
    <h3> [IMDB] 영화제 별 수상 이력 수집 </h3>

    IMDB Crawler를 통해 영화제별 수상 이력을 ~/.datas/IMDb/ 에 저장합니다.
    
    해당 endPoint에서 서비싱 하고 있는 영화제 리스트와 이름은 아래와 같습니다.

    - 아카데미 (1929 ~ ) event이름 : academy 매년 5월 업데이트 
    - 칸 (1939 ~ ) event이름 : cannes 매년 7 월 업데이트
    - 베니스 (1932 ~ ) event이름 : venice 매년 10 월 업데이트
    - 부산 (1996 ~ ) event이름 : busan 매년 11 월 업데이트


    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Year <br> 
    **Recommand call** : 1 call per day<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/imdb/award?event={event_name}&year={wanted_year}'
    ```
    """
    return get_awards(event, year) 

# 일별 + 지역 코드 일별 박스오피스 순위 및 정보 수집
@router.get("/kobis/daily-boxoffice")
async def get_daily_box_office_routes(now_date:str, area_code:str):
    """
    <h3> [KOBIS] 국내 박스오피스 순위 및 기타 정보 수집 </h3>

    KOBIS API 를 통해 일별/지역별 박스오피스 순위 및 기타 정보를 ~/.datas/KOBIS/ 에 저장합니다.


    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : 1 Day <br> 
    **Recommand call** : 1 call per day<br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/kobis/daily-boxoffice?now_date=2023-01-01&area_code={DB_areaCode}'
    ```
    """
    return get_daily_box_office(now_date, area_code)

# 기본 지역 코드 DB 적재
@router.get("/kobis/baseArea-code")
async def update_movie_location_code_routes():
    """
    <h3> [KOBIS] KOBIS 데이터 수집에 사용되는 지역 코드 DB update </h3>

    KOBIS API 를 통해 일별/지역별 박스오피스 순위 및 기타 정보를 ~/.datas/KOBIS/ 에 저장합니다.


    ```
    .
    ├── IMDb
    │   └── bin
    ├── TMDB
    │   ├── discover
    │   ├── credit
    │   ├── detail
    │   ├── images
    │   ├── lists
    │   ├── people_detail
    │   └── similar
    ├── kobis
    ├── kopis
    └── spotify
    ```

    **Update Frequency** : @once <br><br>
    **Example CURL 주소**
    ```shell
    curl 'https://{IP}:{port}/kobis/baseArea-code'
    ```
    """
    return update_movie_location_code()

