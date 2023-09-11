
def mysql_connector():
    from configparser import ConfigParser
    from mysql import connector
    # import MySQLdb

    parser = ConfigParser()
    config_dir = '/home/hooniegit/config/config.ini'
    parser.read(config_dir)

    MYSQL_HOST = parser.get('MYSQL', 'MYSQL_HOST')
    MYSQL_PWD = parser.get('MYSQL', 'MYSQL_PWD')
    MYSQL_PORT = parser.get('MYSQL', 'MYSQL_PORT')
    MYSQL_USER = parser.get('MYSQL', 'MYSQL_USER')
    MYSQL_DB = parser.get('MYSQL', 'MYSQL_DB')

    print(MYSQL_PWD)

    conn = connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PWD,
        database=MYSQL_DB
    )

    print("mysql connection created")
    return conn


def mysql_connectionPool():
    from configparser import ConfigParser
    from mysql.connector.pooling import MySQLConnectionPool

    parser = ConfigParser()
    config_dir = '/home/hooniegit/config/config.ini'
    parser.read(config_dir)

    MYSQL_HOST = parser.get('MYSQL', 'MYSQL_HOST')
    MYSQL_PWD = parser.get('MYSQL', 'MYSQL_PWD')
    MYSQL_PORT = parser.get('MYSQL', 'MYSQL_PORT')
    MYSQL_USER = parser.get('MYSQL', 'MYSQL_USER')
    MYSQL_DB = parser.get('MYSQL', 'MYSQL_DB')

    pool = MySQLConnectionPool(
    pool_name="mypool",
    pool_size=12,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PWD,
    database=MYSQL_DB
    )

    print("mysql connection pool created")
    return pool


if __name__ == '__main__':
    conn = mysql_connector()