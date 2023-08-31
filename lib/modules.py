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