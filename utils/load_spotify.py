import json, requests, configparser

def get_token():

    config = configparser.ConfigParser()
    config.read('config/config.ini')

    client_id = config.get('SPOTIFY', 'client_id')
    client_sc = config.get('SPOTIFY', 'client_sc')

    # requests
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_sc}'.encode()
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()
 
    # return access token
    access_token = response['access_token']
    return access_token

#movie_id 를 DB에서 빨아온 movie_nm 으로 교체 후 진행
def get_soundtrack(movie_name, access_token):

    search = movie_name

    # requests
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    params = {
        'q' : search,
        'type': 'album',
        'limit' : "3"
    }
    response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers).json()

    # file save
    data_path = "<data_폴더_절대경로>"
    json_name = f"spotify_{movie_id}.json"
    json_path = f"{data_path}/{json_name}"
    with open(json_path, "w") as file:
        json.dump(response, file, indent=4, ensure_ascii=False)