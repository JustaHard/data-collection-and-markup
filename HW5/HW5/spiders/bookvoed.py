import scrapy
from scrapy.exporters import JsonItemExporter


class BookvoedSpider(scrapy.Spider):
    name = "bookvoed"
    allowed_domains = ["www.bookvoed.ru"]
    start_urls = ["https://www.bookvoed.ru/catalog"]

    def parse(self, response):
        books = response.xpath('//div[@class="product-card"]')

        for book in books:
            url = book.xpath('./div/a[contains(@class, "ui-link")]/@href').get()
            yield response.follow(url, callback=self.parse_book)

        next_page_link = response.xpath('//li[contains(@class, "next")]/a/@href').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    def parse_book(self, response):
        url = response.url
        name = response.xpath('//h1/text()').get()
        author = response.xpath('//h2[@class="ui-comma-separated-links__tag"]/text()').get()
        price = (int(''.join(response
                             .xpath('//div[@class="price-block-price-info__price"]/span[1]/text()')
                             .get().split()[:-1])))
        yield {
            'url': url,
            'name': name,
            'author': author,
            'price': price
        }