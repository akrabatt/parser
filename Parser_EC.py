import requests
from bs4 import BeautifulSoup
import xlwt


URL = [
        'https://stv39.ru/catalog/avtomatika_i_shchity/',
        'https://stv39.ru/catalog/kabel/',
        'https://stv39.ru/catalog/lampy/',
        'https://stv39.ru/catalog/osvetitelnoe_oborudovanie/',
        'https://stv39.ru/catalog/izmeritelnye_pribory_i_instrumenty/',
        'https://stv39.ru/catalog/elektro_ustanovochnye_izdeliya/',
        'https://stv39.ru/catalog/instrumenty/',
        'https://stv39.ru/catalog/klimat_kontrol/',
        'https://stv39.ru/catalog/bytovye_i_sadovye_tovary/',
        'https://stv39.ru/catalog/elektromontazhnye_izdeliya_i_kabelnye_sistemy/',
        'https://stv39.ru/catalog/stroitelnoe_oborudovanie_osnastka_i_materialy/'
       ]  # указываем юрл адрес страницы которую будем парсить
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '  # словарь в котором мы отправляем заголовки, чтобы сервер не посчитал нас за ботов
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',  # ищем их в разделе сеть кода страницы
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/'
                     'webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}  # словарь в котором мы отправим заголовки
FILE = 'eq_EC.xls'
HOST = 'https://stv39.ru'

equipment = []
equipment_1 = []

book_for_write = xlwt.Workbook('utf8')  # создаём книгу
sheet_for_write = book_for_write.add_sheet('ОБОРУДОВАНИЕ_EC')  # создаём лист в этой книге


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
        try:
            link = HOST + item.find('a', class_='b-catalog-items-item__link').get('href')
            title_value = item.find('a', class_='b-catalog-items-item__link').get_text(strip=True)
            price_value = item.find('div', class_='bx_price b-catalog-items-item__price').get_text(strip=True).replace(' руб.', '')
            equipment.append({
                'title': title_value,
                'price': price_value,
                'link': link
            })
        except AttributeError:
            price_value = item.find('a', class_='bx_bt_button bx_medium b-catalog-items-item-hover_'
                                                '_to-notify bx-catalog-subscribe-button not-available-btn').get_text(strip=True)
            # price_value = 'нет в наличии, товар под заказ'
            equipment.append({
                'title': title_value,
                'price': price_value,
                'link': link
            })
    return equipment


'''запись файла'''
def save_file(eq):
    a = 0
    for i in range(len(equipment)):
        title = equipment[i]['title']
        price = equipment[i]['price']
        link = equipment[i]['link']
        sheet_for_write.write(a, 0, title)
        sheet_for_write.write(a, 1, price)
        sheet_for_write.write(a, 2, link)
        a += 1


'''запускаем'''
def parse1():
    for u in range(len(URL)):
        html = get_html(URL[u])
        if html.status_code == 200:
            print('Доступ к html. Статус: Успешно')
            pages_count = get_pages_count(html.text)
            for page in range(1, pages_count + 1):
                print(f'Парсинг страницы {page} из {pages_count}...')
                html = get_html(URL[u], params={'PAGEN_2': page})
                equipment_1.extend(get_content(html.text, equipment))
            print(len(equipment))
        else:
            print('Доступ к html. Статус: Ошибка')
    save_file(equipment)
    book_for_write.save('{0}.xls'.format(FILE))  # сохраняем книгу
    print('файл сохранён')


# parse1()





