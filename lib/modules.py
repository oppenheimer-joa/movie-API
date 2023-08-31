import configparser, mysql.connector, boto3

def get_config(group, req_var):
	config = configparser.ConfigParser()
	config.read('config/config.ini')
	result = config.get(group, req_var)

	return result


def db_conn(charset=True):

	host = get_config('MYSQL', 'MYSQL_HOST')
	user = get_config('MYSQL', 'MYSQL_USER')
	password = get_config('MYSQL', 'MYSQL_PWD')
	database = get_config('MYSQL', 'MYSQL_DB')
	port = get_config('MYSQL', 'MYSQL_PORT')

	if charset:
		conn = mysql.connector.connect(host=host,
									user=user,
									password=password,
									database=database,
									port=port)

	else :
		conn = mysql.connector.connect(host=host,
									user=user,
									password=password,
									database=database,
									port=port,
									charset='utf8mb4')

	return conn

def create_s3client():
    
    access = get_config("AWS", "S3_ACCESS")
    secret = get_config("AWS", "S3_SECRET")

    # s3 client 생성
    s3 = boto3.client('s3', aws_access_key_id=access,
        aws_secret_access_key=secret)
        
    return s3