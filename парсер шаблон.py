import requests  # импортируем бибилиотеки для парсера
from bs4 import BeautifulSoup
import csv

URL = ''  # указываем юрл адрес страницы которую будем парсить
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '  # словарь в котором мы отправляем заголовки, чтобы сервер не посчитал нас за ботов
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',  # ищем их в разделе сеть кода страницы
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
                     'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}  # словарь в котором мы отправим заголовки
FILE = 'obor.csv'

def get_html (url, params=None ):  # 1 аргумент это юрл страницы с которой необходимо получить контент, парамс опциональный аргумент(по умолчанию ноль) передавать дополнительные аргументы
    r = requests.get(url, headers=HEADERS, params=params)  # выполняем гет запрос, 1й пр. отпр переданный юрл, потом заголовки и параметры
    return r  # возвращаем объект запроса и используем ниже в функции pars


def get_pages_count(html):  # функция принимает html который мы получили выше, функция узнает количество страниц
    soup = BeautifulSoup(html, 'html.parser')  # объект с которым мы будем работать
    pagination = soup.find_all('a', class_='b-catalog-pagination__link')  # создаём объект и получаем ссылки
    if pagination:  # условие на проверку погинации есть ли оно
        return int(pagination[-1].get_text())  # берем последний элемент (последнюю страницу)
    else:
        return 1

def get_content (html):  # принимает html и распарсит
    soup = BeautifulSoup(html, 'html.parser')  # создаём объект soup и обращаемся к конструктору, передаём ему параметры, из него создаются объекты пайтон к которым мы можем обращаться и работать
    items = soup.find_all('li', class_='b-catalog-items-item b1c-ajax')   # получаем объекты items и для этого обращаемся к soup к методу find_all который позволяет получить коллекцию

    obor = []  # список для записи словарей с данными
    for item in items:
        obor.append({
            'title': item.find('a', class_='b-catalog-items-item__link').get_text(strip=True),  # названия оборудования
            'price': item.find('div', class_='bx_price b-catalog-items-item__price').get_text(strip=True)  # цена
        })
    return obor


def save_file(items, path):  # функция сохранения в файл
    with open(path, 'w', newline='') as file:  # указываем путь, w значит запись
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Оборудование', 'Цена'])
        for item in items:
            writer.writerow([item['title'], item['price']])



def parse():  # осн функция в ней будет вызываться всё
    URL = input('введите URL: ')
    URL = URL.strip()
    html = get_html(URL)  # создаём переменную и вызываем функцию, ей передаём юрл параметр
    if html.status_code == 200:  # 200 это значит что мы достучались до страницы
        print('достучались')
        obor1 = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'парсинг страницы {page} из {pages_count}...')  # цикл создан для того чтобы пропарсить все страницы
            html = get_html(URL, params={'PAGEN_2': page})
            obor1.extend(get_content(html.text))
        save_file(obor1, FILE)
        print(f'получено {len(obor1)} оборудования')

            #obor = get_content(html.text)  # вызываем гет контент и передаем ему html и текст, те html готовый с которым будет работать
    else:
        print('что то не то')

parse()