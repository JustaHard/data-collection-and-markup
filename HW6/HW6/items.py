# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, Compose

def process_photo(value):
    try:
        value = value[0].split()[0]
    except Exception as e:
        value = e
    return value

class Hw6Item(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    category_name = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field(input_processor=Compose(process_photo), output_processor=TakeFirst())