import json

from myfirstscraper.items import ProductItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from myfirstscraper.items import ProductPhoneItem


class SpiderKomp(CrawlSpider):
    name = "autokomp"
    allowed_domains = ["komputronik.pl"]
    start_urls = ["https://www.komputronik.pl/category/1596/telefony.html"]

    rules = [
        Rule(LinkExtractor(allow=[r"p=\d+"])),
        Rule(LinkExtractor(allow=["product"]), follow=False, callback="parse_item"),
    ]

    def parse_start_url(self, response):
        return [f"{self.start_urls[0]}/?p=1"]

    def parse_item(self, response):
        get_json_with_brand = (
            response.xpath('//script[contains(text(),"brand")]/text()').get().strip()
        )
        json_data = json.loads(get_json_with_brand) if get_json_with_brand else {}

        loader = ProductItemLoader(item=ProductPhoneItem(), response=response)
        loader.add_css("name", "section#p-inner-name h1::text")
        loader.add_value("price", json_data)
        loader.add_value("vendor", json_data)
        yield loader.load_item()
