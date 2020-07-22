import requests
from bs4 import BeautifulSoup
import xlrd
import xlwt

URL = [
    # 'https://www.megapolys.com/catalog/stroitelnye_materialy/',
    # 'https://www.megapolys.com/catalog/tovary_dlya_dachi_i_sada/',
    # 'https://www.megapolys.com/catalog/elektrooborudovanie/',
    # 'https://www.megapolys.com/catalog/otoplenie_i_vodosnabzhenie/',
    # 'https://www.megapolys.com/catalog/napolnye_pokrytiya/',
    # 'https://www.megapolys.com/catalog/tovary_dlya_doma_i_byta/',
    # 'https://www.megapolys.com/catalog/dekorativno_otdelochnye_materialy/',
    # 'https://www.megapolys.com/catalog/stolyarnye_izdeliya/',
    # 'https://www.megapolys.com/catalog/santekhnika/',
    # 'https://www.megapolys.com/catalog/instrumenty_tekhnika/',
    # 'https://www.megapolys.com/catalog/avtotovary/',
    # 'https://www.megapolys.com/catalog/osveshchenie/',
    # 'https://www.megapolys.com/catalog/plitka/',
    'https://www.megapolys.com/catalog/tekhnicheskie_sredstva_bezopasnosti/',
    # 'https://www.megapolys.com/catalog/tekhno_siti_1/'
]

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
              ',image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

FILE = ''
HOST = 'https://www.megapolys.com'

book = xlrd.open_workbook('./eq_EC.csv.xls', formatting_info=True)
sheet = book.sheet_by_index(0)
sheet1 = xlwt.Workbook.sheet()

equipment = []
equipment_1 = []


'''получаем html'''
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



'''получаем количество страниц'''
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='dark_link')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


'''получаем контент ='''
def get_content(html, equipment):

    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_= 'item_block col-4 col-md-3 col-sm-6 col-xs-6')
    for item in items:
        try:
            link = HOST + item.find('a', class_='dark_link').get('href')
            title_value = item.find('div', {'class': 'item-title'}).get_text(strip=True)  # используем другой способ поиска
            price_value = item.find('span', class_='price_value').get_text(strip=True)

            equipment.append({
                'title': title_value,
                'price': price_value,
                'link': link
            })
        except AttributeError:
            price_value = 'no price'
            equipment.append({
                'title': title_value,
                'price': price_value,
                'link': link
            })
    return equipment


'''сохраняем В файл'''
def save_in_file(eq):
    a = 0
    for i in range(len(equipment)):
        title = equipment[i]['title']
        price = equipment[i]['price']
        link = equipment[i]['link']
        xlwt.sheet1.write(a, 4, title)
        xlwt.sheet1.write(a, 5, price)
        xlwt.sheet1.write(a, 6, link)
        a += 1



'''основная функция'''
def parse():
    for u in range(len(URL)):
        html = get_html(URL[u])
        if html.status_code == 200:
            print('Доступ к html. Статус: Успешно')
            pages_count = get_pages_count(html.text)
            for page in range(1, pages_count + 1):
                print(f'Парсинг страницы {page} из {pages_count}...')
                html = get_html(URL[u], params={'PAGEN_1': page})
                equipment_1.extend(get_content(html.text, equipment))
            # print(equipment)
            print(len(equipment))
        else:
            print('Доступ к html. Статус: Ошибка')
    save_in_file(equipment)
    book.save()
    print('файл сохранён')

parse()
