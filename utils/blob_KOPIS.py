import os, boto3, configparser
from datetime import datetime
from lib.modules import *
    
def blob_kopis(date):
    s3 = create_s3client()

    # KOPIS > date_gte
    date_dt = datetime.strptime(date, "%Y-%m-%d")
    year = date_dt.strftime("%Y")
    server_path = "./datas/kopis"
    datas = os.listdir(server_path)
    for filename in datas:
        if f"{date}" in filename and filename.endswith(".xml"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'kopis/{year}/{filename}')