# -*- coding: utf-8 -*-

# 在这里定义爬虫的models需要获取的信息
# 可以参考 http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExampleItem(scrapy.Item):
    """ExampleItem类是一个模板, 需要将其中的内容替换为爬虫运行时想要存储的待抓取国家信息
    """
    name = scrapy.Field()
    population = scrapy.Field()
