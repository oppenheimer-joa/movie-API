import glob, os


# category = {
#     discoverMovie, movieCredits, movieDetails, 
#     movieImages, movieSimilar, peopleDetail
# }

# 파일명 형식
#기간별 영화 정보 : TMDB_23-08-07_23-08-13_1.json  # <개봉_시작일_앞>_<개봉_시작일_뒤>_<페이지>
#
#영화 상세정보 : TMDB_moviesDetails_1149397_2023-08-25.json  # <영화_ID>, <개봉_시작일_앞>
#영화 출연진 및 제작진 : TMDB_moviesCredits_1149397_2023-08-25.json  # <영화_ID>, <개봉_시작일_앞>
#영화 이미지 : TMDB_moviesImages_1149397_2023-08-25.json  # <영화_ID>, <개봉_시작일_앞>
#영화 관련 작품 목록 : TMDB_moviesSimilar_1149397_2023-08-25.json  # <영화_ID>, <개봉_시작일_앞>
#
#인물 상세정보 : TMDB_peopleDetails_222497_2023-08-25.json  # <인물_ID>, <개봉_시작일_앞>

def TMDB_file_check(xcom:int ,category:str, date:str):
    db_count = xcom
    date = date
    dir = ''
    if category == 'movieCredits' :
        dir = f"./datas/TMDB/credit"
    elif category == 'movieDetails' :
        dir = f"./datas/TMDB/detail"
    elif category == 'movieImages' :
        dir = f"./datas/TMDB/images"
    elif category == 'movieSimilar' :
        dir = f"./datas/TMDB/similar"
    elif category == 'peopleDetail' :
        dir = f'./datas/TMDB/people_detail'
        
    # 해당 경로 내 JSON 파일 리스트
    all_files = glob.glob(os.path.join(dir, "*.json"))
    filtered_files = [f for f in all_files if date in f]
    json_counts = len(filtered_files)

    if category in ['movieCredits', 'movieDetails', 'peopleDetail']:
        if json_counts == db_count :
            return f'{dir} has {json_counts} files'
        else:
            return '1'
    elif category in ['movieImages', 'movieSimilar']:
        if json_counts >= 1 :
            return f'{dir} has {json_counts} files'
        else:
            return '1'