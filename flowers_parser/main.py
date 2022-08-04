import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup as bs
import csv

#   URL сайта, который парсим
URL_TEMPLATE = 'https://bbflowers.ru/catalog/'
#   Запрос к сайту
RESPONSE = requests.get(URL_TEMPLATE)
#   Файл в который выводим итог
FILE_NAME = 'result.csv'
#   Словать для значений характеристик товаров
RESULT_LIST = {
        'flower': [],
        'type': [],
        'href': [],
        'height': [],
        'weight': [],
        'color': [],
        'country': [],
        'plantation': [],
        'count_in_pack': [],
        'availability': [],
        'price': [],
        'price_per_pack': []
        }

    
#   Проверка ответа URL
def check_url(response = RESPONSE):
    try:
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')


#   Возврат списка ссылок каждой страницы каталога
def check_page(response = RESPONSE):
    soup = bs(response.text, "html.parser")
    count_page = soup.find("div", class_="pagination")
    page_href = []
    for page in count_page:
        if len(page.text) == 1:
            page_href.append(URL_TEMPLATE+page.text+'/')
    return page_href



#   Парсинг товаров по URL 
def parse(url):
    
    response = requests.get(url)
    #   Выделение блока items с товарами
    soup = bs(response.text, "html.parser")
    items = soup.find_all("div", class_="item")
    
    #   Поиск в блоке items характеристик товаров
    for data in items:
        
        #   Значения характеристик товаров
        title = data.find(class_='title')
        a = data.find('a')
        height = data.find(class_='value')
        weight = data.find(class_='value').findNext(class_='value')
        flowcolor = data.find(class_='value').findNext(class_='value').findNext(class_='value')
        country = data.find(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value')
        plantation = data.find(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value')
        flowcount = data.find(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value')
        availability =data.find(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value').findNext(class_='value')
        price = data.find(class_='price')
        
        #   Внесение значений товаров в словать
        RESULT_LIST['flower'].append(title.text[ : title.text.find(" ")])
        RESULT_LIST['type'].append(title.text[title.text.find(" ") + 1 : -6])
        RESULT_LIST['href'].append(URL_TEMPLATE+a.get('href')[9:])
        RESULT_LIST['height'].append(height.text)
        RESULT_LIST['weight'].append(weight.text)
        RESULT_LIST['color'].append(flowcolor.text)
        RESULT_LIST['country'].append(country.text)
        RESULT_LIST['plantation'].append(plantation.text)
        RESULT_LIST['count_in_pack'].append(flowcount.text)
        RESULT_LIST['availability'].append(availability.text)
        RESULT_LIST['price'].append(price.text[ : price.text.find(" ")])
        RESULT_LIST['price_per_pack'].append(price.text[price.text.find("(") + 1 : -11])


#   Вывод значений из словаря в файл .csv
def import_to_csv():
    with open(FILE_NAME, 'w', newline='') as csvfile:
        fieldnames = [
            'flower',
            'type',
            'href',
            'height',
            'weight',
            'color',
            'country',
            'plantation',
            'count_in_pack',
            'availability',
            'price',
            'price_per_pack'
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(RESULT_LIST['flower'])):
            writer.writerow(
                {
                    'flower' : RESULT_LIST['flower'][i],
                    'type' : RESULT_LIST['type'][i],
                    'href' : RESULT_LIST['href'][i],
                    'height' : RESULT_LIST['height'][i],
                    'weight' : RESULT_LIST['weight'][i],
                    'color' : RESULT_LIST['color'][i],
                    'country' : RESULT_LIST['country'][i],
                    'plantation' : RESULT_LIST['plantation'][i],
                    'count_in_pack' : RESULT_LIST['count_in_pack'][i],
                    'availability' : RESULT_LIST['availability'][i],
                    'price' : RESULT_LIST['price'][i],
                    'price_per_pack' : RESULT_LIST['price_per_pack'][i],
                    }
                    )


def main():
    check_url(response = RESPONSE)
    for page in check_page(response = RESPONSE):
        parse(page)
    import_to_csv()


if __name__ == "__main__":
	main()