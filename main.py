from bs4 import BeautifulSoup
import csv
import requests
def get_tabl(url, year, month):
    url1=url+str(year)+"/"+str(month)+"/"
    html_text = requests.get(url1, headers=headers).text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.find_all('tr', align='center')
def get_data(map, soup, year, month, id):
    ads_2 = soup.find_all('td')
    data = ads_2[0].text
    data = data + "." + str(month) + "." + str(year)
    map[id] = {}
    map[id]["Дата"] = data
    map[id]["День_температура"] = ads_2[1].text
    map[id]["День_давление"] = ads_2[2].text
    if len(map[id]["День_давление"]) == 1:
        map[id]["День_давление"] = '-'
    if ads_2[5].text == "Ш":
        map[id]["День_ветер"] = "-"
    else:
        map[id]["День_ветер"] = ads_2[5].text
    map[id]["Вечер_температура"] = ads_2[6].text
    map[id]["Вечер_давление"] = ads_2[7].text
    if ads_2[10].text == "Ш":
        map[id]["Вечер_ветер"] = "-"
    else:
        map[id]["Вечер_ветер"] = ads_2[10].text
    return map
def create_result(map, id):
    result=[]
    for i in range(id):
        result.append([])
        result[i].append(str(i + 1))
        result[i].append(str(map[i]["Дата"]))
        result[i].append(str(map[i]["День_температура"]))
        result[i].append(str(map[i]["День_давление"]))
        result[i].append(str(map[i]["День_ветер"]))
        result[i].append(str(map[i]["Вечер_температура"]))
        result[i].append(str(map[i]["Вечер_давление"]))
        result[i].append(str(map[i]["Вечер_ветер"]))
    return result
headers ={
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, lzma, sdch',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
}
year = 2008
map = {}
id = 0
year_2 = 2022
month_2 = 12
while year <= year_2:
    month = 1
    if year == year_2:
        month_2 = 10
    while month <= month_2:
        ads = get_tabl("https://www.gismeteo.ru/diary/4618/", year, month)
        for i in range(len(ads)):
            map=get_data(map, ads[i], year, month, id)
            id += 1
        month+=1
    year+=1

map_2=[["День", "Дата", "День_температура", "День_давление",
       "День_ветер", "Вечер_температура", "Вечер_давление", "Вечер_ветер"]]
with open("data.csv", "w", newline='') as file:
    writer=csv.writer(file, delimiter=';')
    writer.writerows(map_2)
    result=create_result(map, id)
    writer.writerows(result)

