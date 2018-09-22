# -*- coding: utf-8 -*-
import json
import logging
import os
import re

import scrapy
from scrapy.shell import inspect_response

logger = logging.getLogger(__name__)


class ContractSpider(scrapy.Spider):
    name = "contracts"

    addressUrl = "https://etherscan.io/address/{}"
    allowed_domains = ["etherscan.io"]

    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    p = os.path.join(father_path, "contractAddress-20180922-100358.json")
    start_urls = []
    with open(p) as f:
        for i in f.readlines():
            start_urls.append(addressUrl.format(json.loads(i)["address"]))

    custom_settings = {
        "AUTOTHROTTLE_ENABLED": True,
        "LOG_LEVEL": "INFO",
        "COOKIES_ENABLED": False,
    }

    addressR = re.compile(r"address/(\S+)")

    def parse(self, response):
        "Sorry, You have reached your maximum request limit for this resource "
        if "maximum request limit" in response.body_as_unicode():
            # inspect_response(response, self)
            # 重试.
            request = response.request
            if "retry_times_etherscan" in request.meta:
                retry_times_etherscan = request.meta["retry_times_etherscan"]
            else:
                retry_times_etherscan = 0
            retryreq = request.copy()
            retryreq.dont_filter = True
            retryreq.meta["retry_times_etherscan"] = retry_times_etherscan + 1
            retryreq.priority = request.priority + -1
            logger.info(
                "Retrying %(request)s (failed %(retries)d times)",
                {"request": request, "retries": retry_times_etherscan + 1},
            )
            return retryreq
        address = response.url.split("address/")[-1]
        name = response.xpath('//a[@data-placement="bottom"]/text()').extract_first()
        code = response.css("#editor::text").extract_first()
        yield {"name": name, "address": address, "code": code}
