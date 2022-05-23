# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductPhoneItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    vendor = scrapy.Field()
