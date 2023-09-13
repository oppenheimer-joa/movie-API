import os, boto3, configparser
from datetime import datetime
from lib.modules import *
    
def blob_spotify(date:str):
    s3 = create_s3client()

    # Spotify > year
    server_path = "./datas/spotify"
    datas = os.listdir(server_path)
    for filename in datas:
        if f"{date}" in filename and filename.endswith(".json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'spotify/{date}/{filename}')