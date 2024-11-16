import requests
from fake_useragent import UserAgent
from lxml import html
import csv

# Указываем параметры запроса
url = 'https://gb.ru/posts'
headers = {'User-Agent': UserAgent().chrome}
params = {'page': 1}

# Создаем сессию для маскировки под обычного пользователя
session = requests.Session()

# Создаем пустой массив для записи полученных данных
posts_info = []
while True:
    # Посылаем запрос на получение страницы сайта и преобразуем ее в html формат
    response = session.get(url, params=params, headers=headers)
    tree = html.fromstring(response.content)

    # Получаем список всех постов
    posts = tree.xpath('//div[@class="post-items-wrapper"]/div')

    # Проверяем, имеется ли на текущей странице хотя бы один пост, если нет, завершаем цикл
    if not posts:
        break
    else:
        print(f'Обрабатывается страница {params['page']}')

    # Получаем информацию по каждому посту на странице
    for post in posts:
        info = {
            # Получаем заголовок поста
            'name': (post.xpath('.//div/a[contains(@class, "h3")]')[0].
                    text.encode('latin1').decode('utf-8')),
            # Получаем дату публикации поста
            'date': (post.xpath('.//div/div[contains(@class, "small")]')[1]
                    .text.encode('latin1').decode('utf-8')),
            # Получаем количество просмотров и комментариев
            'views': int(post.xpath('.//div/div/div[contains(@class, "icon-counter")]/span')[0].text),
            'comments': int(post.xpath('.//div/div/div[contains(@class, "icon-counter")]/span')[1].text)
        }

        # Пытаемся получить описание поста, если его нет, присваиваем переменной значение None
        try:
            description = (post.xpath('.//div/div/div[contains(@class, "small")]/span')[0]
                           .text.encode('latin1').decode('utf-8'))
        except AttributeError:
            description = None
        info['description'] = description

        # Сохраняем информацию о посте в общий массив
        posts_info.append(info)
    
    # Изменяем параметр получения запроса, чтобы перейти на следующую страницу
    params['page'] += 1

# Сохраняем полученный массив в виде csv файла
filepath = 'data/HW4.csv' 

with open(filepath, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=posts_info[0].keys())

    # Записываем в файл заголовки
    writer.writeheader()

    # Записываем в файл содержимое массива
    writer.writerows(posts_info)

    print('Данные сохранены')

print(len(posts_info))