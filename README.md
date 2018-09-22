# ico-spider

[download ICO source code](icospider/spiders/tokens.py)  from [etherscan](https://etherscan.io/)


## how to run 

`pip install -r  requirements.txt`

`scrapy crawl tokens -o savedata/tokens.json`

## [增加爬取合约交易数大于1000的所有合约](icospider/spiders/contract.py)

合约地址查询是从 google bigquery拿到的[链接](https://bigquery.cloud.google.com/savedquery/348440405491:0fa9ddc95468404b8d291d09873af279)

## 增加反爬手段
1. 增加浏览器头
2. 自动限速
3. 被禁止后，自动重试