#!/usr/bin/env python
# coding:utf-8

"""
串行下载测试脚本
"""

from mongo_cache import MongoCache
from link_crawler import link_crawler
from alexa_urls_class import AlexaCallback


def main():
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    link_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache)


if __name__ == '__main__':
    main()
