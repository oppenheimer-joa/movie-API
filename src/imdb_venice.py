import requests, re, json, os
from bs4 import BeautifulSoup as bs
import datetime

save_path = "/Users/woorek/Downloads/tmp_json/"

start_year = 2020
end_year = int(datetime.datetime.today().strftime("%Y"))


header = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
params = {
        "ref_":"fea_eds_top-1_3"
    }

# for i in range(2022,end_year+1):
for i in range(start_year,end_year+1):
    url = f"https://www.imdb.com/event/ev0000681/{i}/1/"

    resp = requests.get(url=url, headers=header, params=params).text
    soup = bs(resp, "html.parser")

    script_tags = soup.select('#main > div:nth-child(5) > span > script')

    data = str(script_tags[0])
    tmp_data = (((data.split(">")[1]).split("<")[0]).split("IMDbReactWidgets.NomineesWidget.push(['center-3-react',")[1]).split("]);")[0]
    final_dict = json.loads(tmp_data)

    file_name = f"venice_{i}.json"
    with open(os.path.join(save_path,file_name), "w") as json_file:
        json.dump(final_dict, json_file, indent=4)

print("끝")