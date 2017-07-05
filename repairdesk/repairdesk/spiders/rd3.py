# -*- coding: utf-8 -*-
import scrapy


class Rd3Spider(scrapy.Spider):
    name = 'rd3'
    allowed_domains = ['https://api.repairdesk.co/api/web/v1/?api_key=mUz8SpB-hyAO-HMxe-NQC9-Gy5oqQ1IR']
    start_urls = ['http://https://api.repairdesk.co/api/web/v1/?api_key=mUz8SpB-hyAO-HMxe-NQC9-Gy5oqQ1IR/']

    def parse(self, response):
        pass
