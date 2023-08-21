import requests
import json
import os

def get_TMDB_data(api_key, page, file_number, year, date_gte, date_lte):
    base_url = "https://api.themoviedb.org/3/discover/movie"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    params = {
        "include_adult": "True",
        "include_video": "True",
        "language": "ko-KR",
        "sort_by": "primary_release_date.desc",
        "page": page,
        # "primary_release_year": year,
        "primary_release_date.gte": date_gte,
        "primary_release_date.lte": date_lte,
        "watch_region": "KR"
    }

    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()
    json_data = response.json()

    if not json_data['results']:
        return f'TMDB_INFO_{year}_{file_number}.json : No Data', None
    else:
        dir = f"/home/kjh/code/Nolan/Data/TMDB/TMDB_INFO_{year}_{file_number}.json"
        with open(dir, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        return f'TMDB_INFO_{year}_{file_number}.json : Data received', json_data['results'][-1]['release_date']

api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZjNlNDI1MmUwYzA0ZTQwNTk4NzcwMmJmY2UxMDFjMiIsInN1YiI6IjY0ZGYyODk5Yjc3ZDRiMTEzZTA2YmY0ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XZ6KVEQwhFBu6gCY04CQPG8T0rWXujPCHJA4GS62dog"
MAX_PAGE_PER_CYCLE = 500

file_number = 1
year = 2023
date_gte = '2023-01-01'
date_lte = '2023-08-20'

while True:
    for page in range(1, MAX_PAGE_PER_CYCLE + 1):
        message, last_release_date = get_TMDB_data(api_key, page, file_number, year, date_gte, date_lte)
        print(message)
               
        if "No Data" in message:
            break

        file_number += 1
        
        if page == 500:
            date_lte = last_release_date
    else:  # if the inner for-loop didn't break due to "No Data", continue to next 500 pages
        continue

    break
