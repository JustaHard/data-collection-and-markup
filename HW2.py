import requests
import json
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from time import sleep

# https://books.toscrape.com/catalogue/page-1.html
url = 'https://books.toscrape.com/catalogue/'
headers = {'User-Agent': UserAgent().firefox}

session1 = requests.Session()

all_books = []
page = 1
while True:
    response = session1.get(url+f'page-{page}.html', headers=headers)
    if response.status_code == 404:
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('li', {'class': 'col-lg-3'})

    for book in books:
        book_info = {}

        name_info = book.find('h3').findChildren()[0]
        book_info['name'] = name_info.get('title')
        book_info['url'] = url + name_info.get('href')

        session2 = requests.Session()
        book_page_resp = session2.get(book_info['url'], headers=headers)
        book_page_soup = BeautifulSoup(book_page_resp.text, 'html.parser')

        book_info['price'] = book_page_soup.find('p', {'class': 'price_color'}).getText()

        quantity_info = book_page_soup.find('table').findChildren('tr')[5].findChildren()[1].getText()
        book_info['quantity'] = int(quantity_info.split()[2][1:])

        book_info['description'] = book_page_soup.find('article').findChildren('p')[3].getText()

        all_books.append(book_info)
    
    print(f'Обработано {page} страниц')
    page += 1

    sleep(1)

print(len(all_books))
with open('data/books.json', 'w', encoding='utf-8') as file:
    json.dump(all_books, file, ensure_ascii=False, indent=4)