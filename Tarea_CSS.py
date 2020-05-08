# -*- coding: utf-8 -*-
"""
Created on Sat May  2 09:38:05 2020

@author: evillagran
"""

import scrapy

from scrapy.item           import Field, Item
from scrapy.spiders        import CrawlSpider

def remove_whitespace(value):
    return value.strip()


class US_Data_Item(Item):
    Title = Field()
    Link  = Field()
    Body  = Field()
    

class US_Data_SubItem(Item):
    Title       = Field()
    Paragraph   = Field()

   
class USDataCrawler(CrawlSpider):
    name            = "Tarea_Crawling"
    start_urls      = ["https://catalog.data.gov"]
    allowed_domains = ['catalog.data.gov']
    
    custom_settings = {
#                       'CLOSESPIDER_ITEMCOUNT': 100
                       'CLOSESPIDER_PAGECOUNT' : 40,
                       'FEED_FORMAT': 'json',
                       'FEED_EXPORT_INDENT': 1,
                       'FEED_URI':'USData.json'
                       }
       
    def parse(self, response):        
        for link in response.css('.dataset-content'):
            Title = link.xpath('.//h3/a/text()').extract(),               
            Link  = response.urljoin(link.xpath('.//h3/a/@href').extract_first() )
            yield response.follow(Link,callback=self.parse_detail, meta={'Link' : Link,'Title':Title})

        next_page=response.css('.module .pagination li:last-child ::attr(href)').extract_first()
        if next_page is not None:
            next_page_link= response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)

    def parse_detail(self, response):
        lista = US_Data_Item()
        item  = US_Data_SubItem()

        lista["Link"] = response.meta["Link"]
        item["Title"] = response.meta["Title"]
        item["Paragraph"]  = list()

        for text in response.css("p::text").extract():
            item["Paragraph"].append(text.strip())
        
        lista["Body"] = item
        return lista
