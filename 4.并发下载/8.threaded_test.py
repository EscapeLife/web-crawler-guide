#!/usr/bin/env python
# coding:utf-8

import sys
from threaded_crawler import threaded_crawler
from mongo_cache import MongoCache
from alexa_urls_class import AlexaCallback


def main(max_threads):
    scrape_callback = AlexaCallback()
    cache = MongoCache()
    # cache.clear()
    threaded_crawler(scrape_callback.seed_url, scrape_callback=scrape_callback, cache=cache, max_threads=max_threads, timeout=10)


if __name__ == '__main__':
    max_threads = int(sys.argv[1])
    main(max_threads)


"""
    test way
    $ time python threaded_test.py 5
"""
