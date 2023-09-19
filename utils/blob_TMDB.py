import os, boto3, configparser
from datetime import datetime
from lib.modules import *

def blob_tmdb(category, date_gte):
    server_path = ""
    if category == 'movieCredits':
        server_path = "./datas/TMDB/credit"
        s3_path = "credit"
    elif category == 'movieDetails':
        server_path = "./datas/TMDB/detail"
        s3_path = "detail"
    elif category == 'movieImages':
        server_path = "./datas/TMDB/images"
        s3_path = "image"
    elif category == 'movieSimilar':
        server_path = "./datas/TMDB/similar"
        s3_path = "similar"
    elif category == 'peopleDetail':
        server_path = "./datas/TMDB/people_detail"
        s3_path = "people_detail"
        
    
    s3 = create_s3client()

    # TMDB > date_gte
    datas = os.listdir(server_path)
    for filename in datas:
        if filename.endswith(f"{date_gte}.json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'TMDB/{s3_path}/{date_gte}/{filename}')


'''
def blob_tmdb_credit(date_gte):
    s3 = create_s3client()

    # TMDB > date_gte
    server_path = "./datas/TMDB/credit"
    datas = os.listdir(server_path)
    for filename in datas:
        if filename.endswith(f"{date_gte}.json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'TMDB/credit/{date_gte}/{filename}')


def blob_tmdb_detail(date_gte):
    s3 = create_s3client()

    server_path = "./datas/TMDB/detail"
    datas = os.listdir(server_path)
    for filename in datas:
        if filename.endswith(f"{date_gte}.json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'TMDB/detail/{date_gte}/{filename}')


def blob_tmdb_images(date_gte):
    s3 = create_s3client()

    server_path = "./datas/TMDB/images"
    datas = os.listdir(server_path)
    for filename in datas:
        if filename.endswith(f"{date_gte}.json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'TMDB/images/{date_gte}/{filename}')


def blob_tmdb_similar(date_gte):
    s3 = create_s3client()

    server_path = "./datas/TMDB/similar"
    datas = os.listdir(server_path)
    for filename in datas:
        if filename.endswith(f"{date_gte}.json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'TMDB/similar/{date_gte}/{filename}')


def blob_tmdb_peopleDetail(date_gte):
    s3 = create_s3client()

    server_path = "./datas/TMDB/people_detail"
    datas = os.listdir(server_path)
    for filename in datas:
        if filename.endswith(f"{date_gte}.json"):
            file_dir = f"{server_path}/{filename}"
            s3.upload_file(file_dir, 'sms-basket', f'TMDB/people_detail/{date_gte}/{filename}')
'''