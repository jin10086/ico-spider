# -*- coding: utf-8 -*-
import scrapy


class TokensSpider(scrapy.Spider):
    name = "tokens"
    allowed_domains = ["etherscan.io"]
    start_urls = ["https://etherscan.io/tokens/"]
    addressUrl = "https://etherscan.io/address/{}"
    nextPageUrl = "https://etherscan.io/{}"
    custom_settings = {"AUTOTHROTTLE_ENABLED": True}

    def parse(self, response):
        tokens = response.css("a").re("/token/(0x\w+)")
        tokens = list(set(tokens))
        for token in tokens:

            yield scrapy.Request(
                self.addressUrl.format(token),
                callback=self.getCode,
                meta={"address": token},
            )

        nextpage = response.xpath('//a[text()="Next"]/@href').extract_first()
        if nextpage:
            yield scrapy.Request(self.nextPageUrl.format(nextpage, callback=self.parse))

    def getCode(self, response):
        name = response.xpath('//a[@data-placement="bottom"]/text()').extract_first()
        address = response.meta["address"]
        code = response.css("#editor::text").extract_first()
        yield {"name": name, "address": address, "code": code}
