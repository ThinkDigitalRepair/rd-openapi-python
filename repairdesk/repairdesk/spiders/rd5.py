# -*- coding: utf-8 -*-
import scrapy


class Rd5Spider(scrapy.Spider):
    name = 'rd5'
    allowed_domains = ['api.repairdesk.co/']
    start_urls = ['http://api.repairdesk.co//']

    def parse(self, response):
        pass
