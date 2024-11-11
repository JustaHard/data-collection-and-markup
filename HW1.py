import requests
import pandas as pd
import os
from dotenv import load_dotenv

def show_categories():    
    start = 0
    step = 50

    while start < len(df):
        print(df.iloc[start:start+step])
        user_input = input('Введите + для перехода на следующую страницу,\n- для перехода на предыдущую страницу\nили q для выхода из просмотра таблицы: ')
        if user_input == '+':
            start += step
        elif user_input == '-' and start != 0:
            start -= step
        elif user_input == 'q':
            break

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists:
    load_dotenv(dotenv_path)

URL = 'https://api.foursquare.com/v3/places/search'

df = pd.read_csv('./data/places-and-apiv3-categories.csv')
category_not_found = True
while category_not_found:
    try:
        CATEGORY = int(input('Введите ID категории, 0 для получения списка категорий или\n-1 для получения списка мест без привязки к категории: '))
        if CATEGORY == 0:
            show_categories()
        elif CATEGORY in list(df['Category ID']) or CATEGORY == -1:
            category_not_found = False
    except:
        pass


HEADERS = {
    'accept': 'application/json',
    'Authorization': os.getenv('API_KEY')
}
PARAMS = {
    'sort': 'RATING',
    'limit': 10
}
if CATEGORY != -1:
    PARAMS['category'] = CATEGORY

response = requests.get(URL, 
                        params=PARAMS, 
                        headers=HEADERS)

if response.ok:
    json_r = response.json()

    places = json_r['results']
    
    i = 1
    for place in places:
        try:
            place_name = place['name']
        except:
            place_name = '*название не найдено*'
        
        try:
            place_address = place['location']['address']
        except:
            place_address = '*точный адрес не найден*'

        try:
            place_rating = place['rating']
        except:
            place_rating = '*нет данных о рейтинге заведения*'

        print(f'{i}. {place_name} - {place_address} - {place_rating}')
        i += 1
else:
    print(f'Ошибка {response.status_code}')
    if response.status_code == 401:
        print('Создайте файл .env в текущей директории и сохраните в нем свой API ключ в формате:')
        print("API_KEY = '*ваш API ключ*'")