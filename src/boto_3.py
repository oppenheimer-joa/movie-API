import boto3, configparser

config = configparser.ConfigParser()
config.read("/home/hooniegit/config/config.ini")

access = config.get("AWS", "S3_ACCESS")
secret = config.get("AWS", "S3_SECRET")

# s3 = boto3.client('s3', aws_access_key_id=access,
#     aws_secret_access_key=secret)
# s3.upload_file('/home/hooniegit/TMDB_peopleDetails_999606_1960-01-22.json', 'sms-basket', 'TMDB/people/1960-01-22/TMDB_peopleDetails_999606_1960-01-22.json')


s3r = boto3.resource('s3', aws_access_key_id=access,
    aws_secret_access_key=secret).meta.client
s3r.upload_file('/home/hooniegit/TMDB_peopleDetails_999606_1960-01-22.json', 'sms-basket', 'TMDB/people/1960-01-22/TMDB_peopleDetails_999606_1960-01-22.json')
