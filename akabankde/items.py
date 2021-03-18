import scrapy


class AkabankdeItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
