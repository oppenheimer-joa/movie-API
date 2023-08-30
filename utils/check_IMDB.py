import os

def imdb_file_check(event,start_year):
    file_path = f"/api/datas/IMDb/imdb_{event}_{start_year}.json"
    if os.path.isfile(file_path):
        size = os.path.getsize(file_path)
        if size >= 8000:
            return "0"
    else:
        return "1"
