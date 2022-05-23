import json
import time

import scrapy

from myfirstscraper.items import ProductPhoneItem


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    vendor = scrapy.Field()


class KompSpider(scrapy.Spider):
    name = "komputronik"
    start_urls = ['https://www.komputronik.pl/category/1596/telefony.html']

    def parse(self, response):
        for product_href in response.css('ul.product-entry2-wrap li a.blank-link::attr(href)').getall():
            yield response.follow(product_href, self.parse_product)

        next_page = response.css('div.sp-top-grey i.icon-caret2-right').get()

        if next_page is not None:
            page_number = response.css('li.pgn-active a::text').get()

            url = f'{self.start_urls[0]}/?p={int(page_number) + 1}'

            yield response.follow(url, callback=self.parse)

    def parse_product(self, response):
        phone = ProductPhoneItem()
        get_json_with_brand = response.xpath('//script[contains(text(),"brand")]/text()').get().strip()
        json_data = json.loads(get_json_with_brand)
        phone["name"] = response.css("section#p-inner-name h1::text").get(default='').strip()
        phone["price"] = json_data.get('offers', {}).get('price', 'notfound')
        phone["vendor"] = json_data.get('brand', {}).get('name', 'notfound')
        yield phone
