# -*- coding: utf-8 -*-
import scrapy


class Rd4Spider(scrapy.Spider):
    name = 'rd4'
    allowed_domains = ['api.repairdesk.co/api/web/v1/?api_key=mUz8SpB-hyAO-HMxe-NQC9-Gy5oqQ1IR']
    start_urls = ['http://api.repairdesk.co/api/web/v1/?api_key=mUz8SpB-hyAO-HMxe-NQC9-Gy5oqQ1IR/']

    def parse(self, response):
        pass
