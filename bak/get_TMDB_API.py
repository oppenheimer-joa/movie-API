import requests
import json
import os

def get_TMDB_data(api_key, page, year):
    """
    Fetch the latest movies from TMDB using the discover endpoint.

    Args:
    - api_key (str): Your TMDB API key.
    - page (int): The page number to fetch. Default is 1.

    Returns:
    - dict: A dictionary containing the results.
    """
    base_url = "https://api.themoviedb.org/3/discover/movie"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json"
    }
    params = {
        "include_adult": "True",
        "include_video": "True",
        "language": "ko-KR",
        "sort_by": "primary_release_date.desc",  # Sort by latest release date
        "page": page,
        "primary_release_year": year,
        "watch_region": "KR"
    }

    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()  # Will raise an error if the HTTP request returned an unsuccessful status code
    json_data = response.json()
    
    if not json_data['results']:
        return f'TMDB_INFO_{year}_{page}.json : No Data'
    else:
        # 파일 저장
        dir = f"/home/kjh/code/Nolan/Data/TMDB/TMDB_INFO_{year}_{page}.json"
        with open (dir, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)
        return f'TMDB_INFO_{year}_{page}.json : Data received'
        

# Example usage:
api_key = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1ZjNlNDI1MmUwYzA0ZTQwNTk4NzcwMmJmY2UxMDFjMiIsInN1YiI6IjY0ZGYyODk5Yjc3ZDRiMTEzZTA2YmY0ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XZ6KVEQwhFBu6gCY04CQPG8T0rWXujPCHJA4GS62dog"
# api_key = '5f3e4252e0c04e405987702bfce101c2'

for page in range(1, 501):
    year = 2023
    message = get_TMDB_data(api_key, page, year)
    print(message)
