# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BestbuyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    ItemName = scrapy.Field()
    SalePrice = scrapy.Field()
    Price = scrapy.Field()
    ProductFeature = scrapy.Field()
    ItemLink = scrapy.Field()