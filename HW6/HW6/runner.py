from scrapy.utils.reactor import install_reactor
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from spiders.unsplash import UnsplashSpider

install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')
configure_logging()

settings = get_project_settings()
settings.update({
    'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
    'ROBOTSTXT_OBEY': True,
    'DOWNLOAD_DELAY': 0.5,
    'ITEM_PIPELINES': {
        'pipelines.PhotosPipeline': 300,
    },
    'IMAGES_STORE': 'images',
    'FEEDS': {
        'unsplash.csv': {
            'format': 'csv',
            'encoding': 'utf-8'
        }
    },
    'LOG_LEVEL': 'WARN'
})

process = CrawlerProcess(settings=settings)
process.crawl(UnsplashSpider)
process.start()