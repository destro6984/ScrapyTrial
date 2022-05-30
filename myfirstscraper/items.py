import scrapy
from itemloaders.processors import TakeFirst,MapCompose


class ProductPhoneItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(str.strip), output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    vendor = scrapy.Field(output_processor=TakeFirst())
