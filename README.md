# movie-API
## v1.3.7/rel 

### 전체 기능

- IMDB 수집/적재/삭제 endpoint 구성
- TMDB 수집/적재/삭제 endpoint 구성
- Kopis(공연) 수집/적재/삭제 endpoint 구성
- Kobis(BoxOffice) 수집/적재/삭제 endpoint 구성
- Spotify 수집/적재/삭제 endpoint 구성

### 추가 기능

- Spotify 데이터 저장 관련 날짜 형식 변경


## FileTree
```
.
├── README.md
├── config
│   ├── __init__.py
│   └── config.ini
├── datas
│   ├── IMDb
│   │   └── bin
│   ├── TMDB
│   │   ├── credit
│   │   │   └── bin
│   │   ├── detail
│   │   │   └── bin
│   │   ├── images
│   │   │   └── bin
│   │   ├── lists
│   │   │   └── bin
│   │   ├── people_detail
│   │   │   └── bin
│   │   └── similar
│   │       └── bin
│   ├── __init__.py
│   ├── kobis
│   │   └── bin
│   ├── kopis
│   │   └── bin
│   └── spotify
│       └── bin
├── dockerfile
├── headingPage.html
├── lib
│   └── modules.py
├── main.py
├── requirements.txt
├── routers
│   ├── __init__.py
│   ├── blob_router.py
│   ├── check_router.py
│   ├── cleansing_router.py
│   ├── load_router.py
│   └── test.py
└── utils
    ├── __init__.py
    ├── blob_BoxOffice.py
    ├── blob_IMDB.py
    ├── blob_KOPIS.py
    ├── blob_TMDB.py
    ├── blob_spotify.py
    ├── check_BoxOffice.py
    ├── check_IMDB.py
    ├── check_KOPIS.py
    ├── check_TMDB.py
    ├── check_spotify.py
    ├── cleansing.py
    ├── load_BoxOffice.py
    ├── load_IMDbAwards.py
    ├── load_KOPIS.py
    ├── load_TMDB.py
    └── load_spotify.py
```
