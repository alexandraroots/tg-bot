import requests
from bs4 import BeautifulSoup

url = "https://www.cbr.ru/"
page = requests.get(url)
# Текст html страницы
soup = BeautifulSoup(page.text, "html.parser")
# находим дату, на которую будут показываться курсы
# all_data = soup.findAll("div", class_="col-md-2 col-xs-7 _right")
# latest_date = all_data[0].text
# данные по всем валютам:
all_data_currencies = soup.findAll("div", class_="main-indicator_rate")

# print(all_data_currencies[0])

# print(all_data)
#
print(all_data_currencies[0])
print(type(all_data_currencies[0]))
usd_all = all_data_currencies[0] # юани
#
print(usd_all.findAll("div", class_="col-md-2 col-xs-9 _right mono-num")[0].text)