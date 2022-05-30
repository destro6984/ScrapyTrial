import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader


def get_price(data):
    price = data.get("offers", {}).get("price")
    return float(price) if price else "notfound"


def get_vendor(data):
    return data.get("brand", {}).get("name", "notfound")


class ProductItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    name_in = MapCompose(str.strip)
    price_in = MapCompose(get_price)
    vendor_in = MapCompose(get_vendor)


class ProductPhoneItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    vendor = scrapy.Field()
