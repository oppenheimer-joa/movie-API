import os, boto3, configparser
from datetime import datetime
from lib.modules import *
    
def blob_kobis(date):
    s3 = create_s3client()

    # KOBIS > date_gte
    date_dt = datetime.strptime(date, "%Y-%m-%d")
    year = date_dt.strftime("%Y")
    server_path = "./datas/kobis"
    datas = os.listdir(server_path)
    for filename in datas:
        if filename.startswith(date) and filename.endswith(".json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'kobis/{year}/{filename}')