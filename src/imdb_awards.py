import requests, json
from bs4 import BeautifulSoup


def get_awards(event, year):
    # 영화제 code 받기
    if event == 'academy':
        code = 'ev0000003'
    elif event == 'cannes':
        code = 'ev0000147'
    elif event == 'venice':
        code = 'ev0000681'
    
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    params = {
        'ref_': 'ev_eh'
    }
    # 영화제 코드, 연도로 데이터 요청
    response = requests.get(f'https://www.imdb.com/event/{code}/{year}/1/', params=params, headers=headers).text
    
    # html 파싱
    soup = BeautifulSoup(response,"html.parser")
    
    # 수상 리스트 추출
    script_data = soup.select('#main > div:nth-child(5) > span > script')
    data = str(script_data)
    pr_data = ((data.split(';')[2]).split("IMDbReactWidgets.NomineesWidget.push(['center-3-react',")[1].split('])')[0])
    fn_data = json.loads(pr_data)

    # json 파일로 적재
    dir = f'/home/kjh/code/SMS/movie-API/datas/{event}/imdb_{event}_{year}.json'
    try:
        with open (dir, 'w', encoding="utf-8") as file:
            json.dump(fn_data, file, indent=4)

        return f'imdb_{event}_{year}.json : Data Saved'
    
    except Exception as e:
        return f'imdb_{event}_{year}.json : Failed {str(e)}'

# TEST
if __name__ == "__main__":
    years = [2019, 2020, 2021, 2022, 2023]
    event = 'venice'
    for year in years:
        get_awards(event, year)

