import sys
sys.path.append("/home/hooniegit/git/personal/python-thread-pool/lib")

from mysql_lib import *
from tmdb_mysql_thread import *
from datetime import datetime, timedelta
from threading import Thread
from mysql.connector.pooling import MySQLConnectionPool


def make_dateList(date, days, limit):
    date_list = []
    date_list.append(date)
    date = datetime.strptime(date, "%Y-%m-%d")

    for count in range(1, limit):
        date = date + timedelta(days=days)
        date_str = date.strftime("%Y-%m-%d")
        date_list.append(date_str)

    return date_list

def thread_job(KEY, date):
    conn = pool.get_connection()
    try:
        thread_single(KEY, conn, date)
    except Exception as e:
        print(f"Error for {date}: {e}")
    finally:
        conn.close()

def thread_all(KEY, date_list):
    threads = []
    for date in date_list:
        thread = Thread(target=thread_job, args=(KEY, date))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    

if __name__ == '__main__':

    KEY = get_keys()

    start_date_str = "1997-06-27"
    date_list_base = make_dateList(start_date_str, 70, 137)

    for date in date_list_base:
        date_list = make_dateList(date, 7, 10)

        pool = mysql_connectionPool()
        thread_all(KEY, date_list)
    