'''import json
from pymongo import MongoClient
from pymongo.errors import *
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['books']
info = db.info

with open('data/books.json', 'r', encoding='utf-8') as f:
    books = json.load(f)

for book in books:
    book['_id'] = book['url']
    try:
        info.insert_one(book)   
    except DuplicateKeyError as e:
        print(e)

books = None

high_quantity_books = info.find({'quantity': {'$gt': 20}})
for book in high_quantity_books:
    pprint(book)'''



"""import json
from clickhouse_driver import Client

client = Client('localhost')

client.execute('''
    CREATE TABLE books 
    (
        `name` String,
        `url` String,
        `price` String,
        `quantity` UInt32,
        `description` String
    )
    ENGINE = MergeTree()
    ORDER BY name;
''')

with open('data/books.json', 'r', encoding='utf-8') as f:
    books_info = json.load(f)

insert_data = [(book['name'], book['url'], book['price'], book['quantity'], book['description']) 
               for book in books_info]

client.execute('''
    INSERT INTO books 
    (name, url, price, quantity, description)
    VALUES''', insert_data)"""