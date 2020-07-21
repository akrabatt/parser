import requests
from bs4 import BeautifulSoup
import xlrd
import xlwt

URL = 'https://www.megapolys.com/catalog/stroitelnye_materialy/'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
              ',image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

FILE = ''
HOST = 'https://www.megapolys.com'

equipment = []
equipment_1 = []


'''получаем html'''
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



'''получаем количество страниц'''
def get_pages_count(html):
    pass


'''получаем контент ='''
def get_content(html, equipment):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_= 'item_block col-4 col-md-3 col-sm-6 col-xs-6')
    for item in items:
        link = HOST + item.find('a', class_='dark_link').get('href')
        title_value = item.find('div', {'class': 'item-title'}).get_text(strip=True)  # используем другой способ поиска
        price_value = item.find('span', class_='price_value').get_text(strip=True)

        equipment.append({
            'title': title_value,
            'price': price_value,
            'link': link
        })
    print(equipment)


'''сохраняем В файл'''
def save_in_file():
    pass

'''основная функция'''
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print('Доступ к html. Статус: Успешно')
        get_content(html.text, equipment)
    else:
        print('Доступ к html. Статус: Ошибка')


parse()
