import sys
sys.path.append("/home/hooniegit/git/organization/sms/movie-API/lib")

from box_office_thread import *

def thread_all(KOBIS_KEY, area_code_list, date_list):
    from threading import Thread

    threads = []
    for code in area_code_list:
        thread = Thread(target=thread_single, args=(KOBIS_KEY, code, date_list))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()


if __name__ == "__main__":

    KOBIS_KEY = get_KOBIS_KEY()
    area_code_list = get_area_code_list()
    date_list = make_dateList(date='20200101', days=1, limit=1353)
    
    thread_all(KOBIS_KEY, area_code_list, date_list)