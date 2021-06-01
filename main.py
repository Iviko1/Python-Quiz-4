from bs4 import BeautifulSoup
import requests
import csv
from time import sleep
from random import randint

def get_page(url):
    res = requests.get(url)

    if not res.ok:
        print(f'Server Response: {res.status_code}')
    else:
        return BeautifulSoup(res.text, 'html.parser')


def get_detail_data(soup):
    try:
        try:
            item_title = soup.find('h1', id='itemTitle').text.replace('Details about', '').strip()
        except:
            item_title = soup.find('h1', class_='product-title').text.strip()
    except:
        item_title = ''

    try:
        try:
            item_currency, item_price = soup.find('div', class_='display-price').text.split('$')
        except:
            try:
                item_currency, item_price = soup.find('span', id='prcIsum').text.split(' ')
            except:
                item_currency, item_price = soup.find('span', id='mm-saleDscPrc').text.split(' ')
    except:
        item_price = ''
        item_currency = ''
    data = {
        'title': item_title,
        'price': item_price,
        'currency': item_currency
    }
    return data


def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []
    item_urls = [link.get('href') for link in links]
    return item_urls


def write_csv(data, item_url):
    with open('data.csv', 'a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        row = [data['title'], data['price'], data['currency'], item_url]
        writer.writerow(row)


def main():
    page = int(input('From which page would you like to start? :'))
    page_count = int(input('How many pages would you like to scrape? :'))
    page_limit = page + page_count
    while page < page_limit:
        url = f'https://www.ebay.com/b/Computer-Graphics-Cards/27386/bn_661796?LH_BIN=1&rt=nc&_pgn={page}'
        products = get_index_data(get_page(url))
        print(f'Scraping Page {page}...')
        for item_url in products:
            data = get_detail_data(get_page(item_url))
            write_csv(data, item_url)
        print(f'Page {page} Done!')
        page += 1
        if page != page_limit:
            sleep_time = randint(5, 10)
            print(f'Sleeping for {sleep_time} seconds to look human :P')
            sleep(sleep_time)


if __name__ == '__main__':
    print('Ebay GPU Price Scraper')
    main()
