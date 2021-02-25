import scrapy

from scrapy.loader import ItemLoader
from ..items import ArgentanlItem
from itemloaders.processors import TakeFirst


class ArgentanlSpider(scrapy.Spider):
	name = 'argentanl'
	start_urls = ['https://www.argenta.nl/blog']

	def parse(self, response):
		post_links = response.xpath('//a[@class="blogTeaser-item"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="title-withborder"]/text()').get()
		description = response.xpath('//div[@class="richtext margBtm40"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="blogDate margBtm20"]/span/text()').get()
		date = date.split(',')[1]

		item = ItemLoader(item=ArgentanlItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
