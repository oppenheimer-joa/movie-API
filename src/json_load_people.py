import sys
sys.path.append("/home/hooniegit/git/personal/python-thread-pool/lib")

from mysql_lib import *
from tmdb_people_thread import *


def make_dateList(date, days, limit):
    from datetime import datetime, timedelta

    date_list = []
    date_list.append(date)
    date = datetime.strptime(date, "%Y-%m-%d")

    for count in range(1, limit):
        date = date + timedelta(days=days)
        date_str = date.strftime("%Y-%m-%d")
        date_list.append(date_str)

    return date_list

def thread_job(KEY, date):
    conn = mysql_connector()
    try:
        thread_single(KEY, conn, date)
    except Exception as e:
        print(f"Error for {date}: {e}")
    conn.close()


def thread_all(KEY, date_list):
    from threading import Thread

    threads = []
    for date in date_list:
        thread = Thread(target=thread_job, args=(KEY, date))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


# need to do until 64
if __name__ == "__main__":

    # start_date_str = "2000-01-"
    # start_date_str = "2005-01-"
    # start_date_str = "2010-01-"
    # start_date_str = "2015-01-"
    # start_date_str = "2020-01-"
    start_date_str = sys.argv[1]
    date_list_base = make_dateList(start_date_str, 273, 14)

    cnt = sys.argv[2]
    KEY = get_keys(cnt)

    for date in date_list_base:
        date_list = make_dateList(date, 7, 39)

        thread_all(KEY, date_list)
