
def extract_academi(year):
    import requests, json
    from bs4 import BeautifulSoup

    # API requests
    url = f'https://www.imdb.com/event/ev0000003/{year}/1/'
    header = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    params = {
        'ref_': 'ev_eh'
    }
    response = requests.get(url, headers=header, params=params).text

    # Page Parse
    soup = BeautifulSoup(response, "html.parser")

    # Data Parse
    movie_div = soup.select("#main > div:nth-child(5) > span > script")
    data = str(movie_div).split('[<script type="text/javascript">')[1]
    data = data.split('IMDbReactWidgets=window.IMDbReactWidgets||{};')[1]
    data = data.split('IMDbReactWidgets.NomineesWidget=IMDbReactWidgets.NomineesWidget||[];')[1]
    data = data.split("IMDbReactWidgets.NomineesWidget.push(['center-3-react',")[1]
    data = data.split("IMDbReactInitialState")[0]
    data = data.split("]);")[0]

    # Data Convert
    json_data = json.loads(data)

    # Data Save
    demo_path = "/Users/kimdohoon/git/openheimer/movie-API/datas/academy" # <- 경로 수정 필요
    file_name = f"imdb_academi_{year}.json"
    file_path = f"{demo_path}/{file_name}"
    with open(file_path, "w") as file:
        json.dump(json_data, file, indent=4)

# TEST
if __name__ == "__main__":
    years = [2023, 2022, 2021, 2020, 2019]
    for year in years:
        extract_academi(year)