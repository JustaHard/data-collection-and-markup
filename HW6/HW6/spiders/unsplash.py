import scrapy
from scrapy.loader import ItemLoader

try:
    from items import Hw6Item
except:
    pass

try:
    from ..items import Hw6Item 
except:
    pass

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        links = response.xpath('//div[@class="bugb2"]/figure/div/a/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_photo)

    def parse_photo(self, response):
        loader = ItemLoader(item=Hw6Item(), response=response)

        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('category_name', '//a[@class="ZTh7D kXLw7"]/text()')
        loader.add_xpath('photo', '//div[@class="rOVXC"]//img[2]/@srcset')       

        return loader.load_item() 