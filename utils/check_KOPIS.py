import os, re, datetime

def kopis_file_check(st_dt:str, db_cnt:int):
    directory_path = "./datas/kopis"
    xml_files_list = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".xml") and st_dt in filename:
            xml_files_list.append(filename)

    xml_file_cnt = len(xml_files_list)

    if xml_file_cnt == db_cnt:
        return f"DB속 개수({db_cnt})와 파일 개수({xml_file_cnt}) 가 같슴둥"
    else:
        return "1"