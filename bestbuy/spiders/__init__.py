# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
from  bestbuy.items import BestbuyItem

class MySpider(scrapy.Spider):
    name = "bestbuy"  # Name of the Spider, required value
    start_urls = ["http://www.bestbuy.com/site/coffee-makers-espresso-machines/multi-cup-coffee-makers/pcmcat258900050007.c?id=pcmcat258900050007"]  # The starting url, Scrapy will request this URL in parse

    for i in range(2,9):
        start_urls.append("http://www.bestbuy.com/site/searchpage.jsp?cp=" + str(i) + '&searchType=search&_dyncharset=UTF-8&ks=960&sc=Global&list=y&usc=All%20Categories&type=page&id=pcat17071&iht=n&seeAll=&browsedCategory=pcmcat258900050007&st=categoryid%24pcmcat258900050007&qp=')
    
    # Entry point for the spider
    def parse(self, response):

        for href in response.css("#main-results > div.list-items > div > div > div.col-xs-3.list-item-thumbnail-column > div > div.thumb a::attr(href)") :
            url = href.extract()
            if "http" not in url:
                url = "http://www.bestbuy.com" + url
            yield scrapy.Request(url, callback=self.parse_item)
 
    # Method for parsing a product page
    def parse_item(self, response):
        
        # Not all deals are discounted (3 cases: a. items on sale with SalePrice shown in the webpage; b. items on sale w/o showing SalePrice in the webpage; c. Regular-season-price items)
        if len(response.css('#priceblock-wrapper-wrapper > div.price-block.priceblock-large > div.pucks-and-price.row > div.col-xs-7 > div.price-column > div.sale-puck').extract()) != 0:
            Price = response.css('#priceblock-wrapper-wrapper > div.price-block.priceblock-large > div.pucks-and-price.row > div.col-xs-7 > div.price-column > div.details > span.regular-price ::text').extract()[0].split('Reg. ')[1][1:-1]
            try:
                SalePrice = response.css('#priceblock-wrapper-wrapper > div.price-block.priceblock-large > div.pucks-and-price.row > div.col-xs-7 > div.price-column > div.item-price ::text').extract()[1]
            except:
                SalePrice = response.css('#price > div.shipping-availability-model').extract()[0].split('data-unit-price="')[1].split('"')[0]
        else:
            SalePrice = -1
            Price = response.css('#priceblock-wrapper-wrapper > div.price-block.priceblock-large > div.pucks-and-price.row > div.col-xs-7 > div.price-column > div.item-price ::text').extract()[1]
        
        # Product Feature
        ProductFeature = ";".join(response.css('#features p::text').extract())
        
        if len(response.css('#features p::text').extract())!=0:
            ProductFeature = ProductFeature + '*'
            ProductFeature = ProductFeature + '~'.join(response.css('#features p::text').extract())
        
        item = BestbuyItem()
        item['ItemName'] = response.css('#sku-title h1::text').extract()[0]
        item['SalePrice'] = SalePrice
        item['Price'] = Price
        item['ProductFeature'] = ProductFeature
        item['ItemLink'] = response.url
        yield item
