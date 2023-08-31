import os, boto3, configparser
from datetime import datetime
from lib.modules import *

def blob_imdb(event, year):
    s3 = create_s3client()

    # IMDB > event, year
    server_path = "./datas/IMDB"
    filename = f"imdb_{event}_{year}.json"
    file_dir = f"{server_path}/{filename}"
    s3.upload_file(file_dir, 'sms-basket', f'IMDb/{filename}')