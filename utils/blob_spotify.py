import os, boto3, configparser
from datetime import datetime
from lib.modules import *
    
def blob_spotify(year):
    s3 = create_s3client()

    # Spotify > year
    server_path = "./datas/spotify"
    datas = os.listdir(server_path)
    for filename in datas:
        if filename.endswith(f"{year}.json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'spotify/{year}/{filename}')