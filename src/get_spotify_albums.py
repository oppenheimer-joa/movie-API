def get_token(client_id, client_sc):
    # module import
    import requests

    # requests
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_sc}'.encode()
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()
 
    # return access token
    access_token = response['access_token']
    return access_token


def get_soundtrack(movie_id, access_token):
    # module import
    import requests, json

    # source file path
    main_path = "<movieDetails_폴더_절대경로>"
    file_name = f"TMDB_movieDetails_{movie_id}.json"
    file_path = f"{main_path}/{file_name}"

    # load source json
    data = json.load(file_path)
    search = data["original_title"]

    # requests
    access_token = "BQC1W9U5wu-ZLGJ4Ko0Y58kvpYe46i4NdXfeq5_kJNN1jnL16y2cZRYeMX4JXb-OOGWL2sqxNS_JC33NLYqKTVbBTwz8BO2E82FzyDviPSFEEVNs55g"
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

# Test
if __name__ == "__main__":
    client_id = "3d918c9fcbe44e099ba189c46cdedd8d"
    client_sc = "9c1ff7f73f4b424ebaf54977cde68f83"

    access_token = get_token(client_id, client_sc)
    get_soundtrack(976573, access_token)