from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import csv

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

try:
    url = "http://books.toscrape.com/"
    driver.get(url)
    time.sleep(2)


    books = []

    while True:

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for book in soup.find_all('article', {'class': 'product_pod'}):
            title = book.find_all('a')[1].get('title')
            price = book.find('p', {'class': 'price_color'}).getText()
            availability = book.find('p', {'class': 'instock availability'}).getText().strip()
            books.append({'Title': title, 'Price': price, 'Availability': availability})

        try:
            next_button = driver.find_element(By.LINK_TEXT, 'next')
            next_button.click()
            time.sleep(2)
        except NoSuchElementException:
            print("Все страницы обработаны.")
            break

    with open('data\books_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Price', 'Availability'])
        writer.writeheader()
        writer.writerows(books)

    print("Данные успешно сохранены в books_data.csv!")

except Exception as e:
    print(f"Ошибка: {e}")

finally:
    driver.quit()
