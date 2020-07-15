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


'''получаем html'''
def get_html (url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


'''получаем количество страниц'''
def get_pages_count(html):
    pass


'''получаем контент'''
def get_content (html, equipment):
    pass


'''запускаем'''
def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print('Доступ к html. Статус: Успешно')
    else:
        print('Доступ к html. Статус: Ошибка')


parse()






