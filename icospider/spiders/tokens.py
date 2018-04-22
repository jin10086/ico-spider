# -*- coding: utf-8 -*-
import scrapy


class TokensSpider(scrapy.Spider):
    name = 'tokens'
    allowed_domains = ['etherscan.io/tokens']
    start_urls = ['http://etherscan.io/tokens/']

    def parse(self, response):
        pass
