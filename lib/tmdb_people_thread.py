
# get_keys(1)
# get_keys(2)
# get_keys(3)
# get_keys(4)
# get_keys(5)
def get_keys(cnt):
    from configparser import ConfigParser

    parser = ConfigParser()
    parser.read('/home/hooniegit/config/config.ini')
    KEY = parser.get("TMDB", f"API_KEY_{cnt}")

    return KEY
    
def make_peopleList(key, conn, date):
    cursor = conn.cursor()

    QUERY = f"""SELECT people_id from people
                WHERE date_gte = '{date}'"""
    cursor.execute(QUERY)
    rows = cursor.fetchall()
    
    people_list = []
    for row in rows:
        people_id = row[0]
        people_list.append(people_id)

    return people_list

def load_json(KEY, conn, people_list, date):
    import json
    import time
    import requests
    
    cursor = conn.cursor()
    for people_id in people_list:
        base_url = f"https://api.themoviedb.org/3/person/{people_id}"
        headers = {
            "Authorization": f"Bearer {KEY}",
            "accept": "application/json"
        }
        response = requests.get(base_url, headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            try:
                dir = f"/home/hooniegit/datas/people/TMDB_peopleDetails_{people_id}_{date}.json"
                with open (dir, "w", encoding="utf-8") as file:
                    json.dump(json_data, file, indent=4, ensure_ascii=False)
            except Exception as e:
                print(e)
        else:
            dir = f"/home/hooniegit/ERROR/people/{date}"
            with open (dir, "w", encoding="utf-8") as file:
                pass
        
        # time.sleep(1)

def thread_single(KEY, conn, date):
    print(f"start thread : {date} >>>>>>")
    people_list = make_peopleList(KEY, conn, date)
    load_json(KEY, conn, people_list, date)
    print(f"<<<<<< end thread : {date}")