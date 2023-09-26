import mysql.connector, configparser, requests
from datetime import datetime, timedelta

def get_keys():
    from configparser import ConfigParser

    parser = ConfigParser()
    parser.read('/home/hooniegit/git/personal/python-thread-pool/config/config.ini')
    KEY = parser.get("TMDB", "API_KEY")

    return KEY
    
def make_peopleList(key, conn, date):
    cursor = conn.cursor()

    QUERY = f"""SELECT movie_id from movie
                WHERE date_gte = '{date}'"""
    cursor.execute(QUERY)
    rows = cursor.fetchall()

    unique_ids = set()
    people_list = []
    
    for row in rows:
        movie_id = row[0]
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {key}"
        }
        response = requests.get(url, headers=headers).json()

        if response.status_code == 200:
            try : cast = response["cast"]
            except : cast = []
            try : crew = response["crew"]
            except : crew = []
            people = crew + cast

            for item in people:
                id_value = item.get("id")
                if id_value not in unique_ids:
                    people_list.append(item)
                    unique_ids.add(id_value)
        else:
            dir = f"/home/hooniegit/ERROR/mysql/{date}"
            with open (dir, "w", encoding="utf-8") as file:
                pass

    # print(len(people_list))    
    return people_list

def insert_people(conn, people_list, date):
    cursor = conn.cursor()

    for person in people_list:
        id = person["id"]
        original_name = person["original_name"]

        QUERY = "INSERT IGNORE INTO people(people_id, people_nm, date_gte) VALUES (%s, %s, %s)"
        values = (id, original_name, date)
        cursor.execute(QUERY, values)
        conn.commit()

def thread_single(KEY, conn, date):
    print(f"start thread : {date} >>>>>>")
    people_list = make_peopleList(KEY, conn, date)
    insert_people(conn, people_list, date)
    print(f"<<<<<< end thread : {date}")