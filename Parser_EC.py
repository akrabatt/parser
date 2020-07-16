import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://stv39.ru/catalog/avtomatika_i_shchity/'  # указываем юрл адрес страницы которую будем парсить
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '  # словарь в котором мы отправляем заголовки, чтобы сервер не посчитал нас за ботов
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',  # ищем их в разделе сеть кода страницы
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
                     'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}  # словарь в котором мы отправим заголовки
FILE = 'ob_EC.csv'

equipment = []
equipment_1 = []


'''получаем html'''
def get_html (url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


'''получаем количество страниц'''
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='b-catalog-pagination__link')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


'''получаем контент'''
def get_content (html, equipment):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('li', class_='b-catalog-items-item b1c-ajax')
    for item in items:
        title_value = item.find('a', class_='b-catalog-items-item__link').get_text(strip=True)
        price_value = item.find('div', class_='bx_price b-catalog-items-item__price').get_text(strip=True)
        equipment.append({
            title_value: price_value
        })
    return equipment


'''сохраняем результаты в прайслист'''
def save_file(items, path):
    pass


'''запускаем'''
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print('Доступ к html. Статус: Успешно')
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            html = get_html(URL, params={'PAGEN_2': page})
            equipment_1.extend(get_content(html.text, equipment))
            print(equipment_1)

    else:
        print('Доступ к html. Статус: Ошибка')


parse()






