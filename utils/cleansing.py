from datetime import datetime, timedelta
import os

# KOBIS(BoxOffice)
def cleanse_daily_box_office(now_date):
	dir_path = "/api/datas/kobis/"
	
	results = []
	for filename in os.listdir(dir_path):
		if now_date in filename and filename.endswith(".json"):
			file_path = os.path.join(dir_path,filename)
			try:
				os.remove(file_path)
				results.append(f"KOBIS : {file_path} : DATA DELETED!")
			except Exception as e:
				results.append(f"KOBIS : {file_path} : DATA NOT DELETED! SOMETHING WENT WRONG!")

	return results


# IMDB
def cleanse_awards(event, year):
	file_path = f"/api/datas/IMDb/imdb_{event}_{year}.json"
	if os.path.isfile(file_path):
		try:
			os.remove(file_path)
			return f"IMDB : {file_path} : DATA DELETED!"

		except Exception as e:
			return f"IMDB : {file_path} : DATA NOT DELETED! SOMETHING WENT WRONG!"


# KOPIS
def cleanse_pf_detail(ST_DT):
	dir_path = "./datas/kopis/"
	
	results = []
	for filename in os.listdir(dir_path):
		if ST_DT in filename and filename.endswith(".xml"):
			file_path = os.path.join(dir_path,filename)
			try:
				os.remove(file_path)
				results.append(f"KOPIS : {file_path} : DATA DELETED!")
			except Exception as e:
				results.append(f"KOPIS : {file_path} : DATA NOT DELETED! SOMETHING WENT WRONG!")

	return results


# SPOTIFY
def cleanse_soundtrack():
	dir_path = "/api/datas/spotify/"
	
	results = []
	for filename in os.listdir(dir_path):
		if filename.endswith(".json"):
			file_path = os.path.join(dir_path,filename)
			try:
				os.remove(file_path)
				results.append(f"SPOTIFY : {file_path} : DATA DELETED!")
			except Exception as e:
				results.append(f"SPOTIFY : {file_path} : DATA NOT DELETED! SOMETHING WENT WRONG!")

	return results


# TMDB
def cleanse_tmdb(category, date):
	if category == "movieCredits":
		dir_path = "./datas/TMDB/credit/"
	elif category == "movieDetails":
		dir_path = "./datas/TMDB/detail/"
	elif category == "movieImages":
		dir_path = "./datas/TMDB/images/"
	elif category == "movieSimilar":
		dir_path = "./datas/TMDB/similar/"
	elif category == "peopleDetail":
		dir_path = "./datas/TMDB/people_detail/"

	results = []

	for filename in os.listdir(dir_path):
		if date in filename and filename.endswith(".json"):
			file_path = os.path.join(dir_path,filename)
			try:
				os.remove(file_path)
				results.append(f"TMDB : {file_path} : DATA DELETED!")
			except Exception as e:
				results.append(f"TMDB : {file_path} : DATA NOT DELETED! SOMETHING WENT WRONG!")

	return results