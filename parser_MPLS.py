import requests
from bs4 import BeautifulSoup
import csv

URL = ''  # указываем юрл для парсинга
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '  # заголовки, чтобы не забанили
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                     'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
FILE = 'ob_MPLS.csv'  # название файла для сохранения


'''функция получения юрл страницы и контента'''
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


'''основная функция, котоая всё вызывает'''
def pars():
    URL = input('введите URL: ')
    html = get_html(URL)
    if html.status_code == 200:
        print('все ок, достучались')


pars()
