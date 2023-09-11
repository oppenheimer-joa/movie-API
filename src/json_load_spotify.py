import sys
sys.path.append("/home/hooniegit/git/personal/python-thread-pool/lib")

from mysql_lib import *
from spotify_thread import *
from datetime import datetime, timedelta
from threading import Thread
from mysql.connector.pooling import MySQLConnectionPool


def thread_all(token, movie_dump):
    threads = []
    for movie_list in movie_dump:
        thread = Thread(target=thread_single, args=(token, movie_list))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


# need to do until 64
if __name__ == "__main__":

    movie_dump = []
    # 1960 / 1970 / 1980 / 1990 / 2000 ..
    start_year = sys.argv[1]

    for i in range(10):
        conn = mysql_connector()
        movie_list = make_movieList(conn, f'{i+start_year}-01-01', f'{(i+1)+start_year}-01-01')
        movie_dump.append(movie_list)
        conn.close()

    cnt = sys.argv[2]
    token = make_accessToken(cnt)
    thread_all(token, movie_dump)
    





