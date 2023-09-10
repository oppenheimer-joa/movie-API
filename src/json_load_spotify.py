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
    for i in range(5):
        conn = mysql_connector()
        movie_list = make_movieList(conn, f'{i+1960}-01-01', f'{(i+1)+1960}-01-01')
        movie_dump.append(movie_list)
        conn.close()

    token = make_accessToken()
    thread_all(token, movie_dump)
    





