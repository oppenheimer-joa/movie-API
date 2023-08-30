import os

def BoxOffice_file_check():
	directory_path = "/api/datas/kobis"
	file_cnt = sum(1 for file in os.listdir(directory_path) if file.endswith('.json'))
	if file_cnt == 17:
		return "0"
	else:
		return "1"
