# -*- coding: utf-8 -*-
import scrapy


class RdSpider(scrapy.Spider):
    name = 'rd'
    allowed_domains = ['https://api.repairdesk.co/api/web/v1/']
    start_urls = ['http://https://api.repairdesk.co/api/web/v1//']

    def parse(self, response):
        pass
