# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZeczecItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    number = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
    backer = scrapy.Field()
    current_funds = scrapy.Field()
    target = scrapy.Field()
    SF = scrapy.Field()
    classify = scrapy.Field()

