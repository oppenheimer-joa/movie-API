import requests, re, json
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}
params = {
    'ref_': 'ev_eh'
}


def cannes_awards(year):
    response = requests.get(f'https://www.imdb.com/event/ev0000147/{year}/1/', params=params, headers=headers).text

    soup = BeautifulSoup(response,"html.parser")

    script_data = soup.select('#main > div:nth-child(5) > span > script')

    data = str(script_data)
    pr_data = ((data.split(';')[2]).split("IMDbReactWidgets.NomineesWidget.push(['center-3-react',")[1].split('])')[0])
    fn_data = json.loads(pr_data)

    dir = f'/home/kjh/code/SMS/movie-API/datas/cannes/imdb_cannes_{year}.json'
    try:
        with open (dir, 'w', encoding="utf-8") as file:
            json.dump(fn_data, file, indent=4)

        return f'imdb_cannes_{year}.json : Data Saved'
    
    except Exception as e:
        return f'imdb_cannes_{year}.json : Failed {str(e)}'

# TEST
if __name__ == "__main__":
    years = [2019, 2020, 2021, 2022, 2023]
    for year in years:
        cannes_awards(year)

