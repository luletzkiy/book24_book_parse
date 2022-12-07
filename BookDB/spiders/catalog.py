from pkg_resources import yield_lines
import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/']

    pages_count = 3210

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://book24.ru/catalog/fiction-1592/page-{page}/'
            yield scrapy.Request(url, callback = self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.product-card__name::attr("href")').extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback = self.parse)

    def parse(self, response, **kwargs):
        item = {
            'title': response.css('.product-detail-page__title::text').extract_first('').strip().split(':', 1)[1].strip(),
            'ISBN' : response.css('.isbn-product::text').extract_first('').strip(),
            'author': response.css('.product-detail-page__title::text').extract_first('').strip().split(':', 1)[0].strip(),
            'description': ' '.join(response.css('.product-about__text p::text').extract()),
            'link': response.url
        }
        yield item
