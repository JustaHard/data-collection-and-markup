# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import hashlib

class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):  
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)

    def file_path(self, request, response = None, info = None, *, item = None):
        try:
            image_url_hash = hashlib.sha1(item['photo'].encode()).hexdigest()
            image_name_wo_spaces = '_'.join(item['name'].split())
            image_filename = f'{image_name_wo_spaces}_{image_url_hash}.jpg'

            return image_filename
        except Exception as e:
            print(e)
