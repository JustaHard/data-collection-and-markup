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
    start_urls = ["https://unsplash.com/t"]

    def parse(self, response):
        categories = response.xpath('//h4/a/@href')
        for category in categories:
            yield response.follow(category, callback=self.parse_category)

    def parse_category(self, response):
        links = response.xpath('//div[@class="bugb2"]/figure/div/a/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_photo)

    def parse_photo(self, response):
        loader = ItemLoader(item=Hw6Item(), response=response)

        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('category_name', '//a[@class="ZTh7D kXLw7"]/text()')
        loader.add_xpath('photo', '//div[@class="rOVXC"]//img[@class="I7OuT DVW3V L1BOa"]/@srcset')       

        return loader.load_item() 