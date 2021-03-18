import scrapy

from scrapy.loader import ItemLoader

from ..items import AkabankdeItem
from itemloaders.processors import TakeFirst


class AkabankdeSpider(scrapy.Spider):
	name = 'akabankde'
	start_urls = ['https://www.akabank.de/de/aka-im-dialog/artikel/archiv/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="h3 teaser__title"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1//text()').get()
		description = response.xpath('(//div[@class="ce-bodytext"])[position()<last()]//text()[normalize-space() and not(ancestor::h1)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=AkabankdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
