#!/usr/bin/env python
# coding:utf-8

import zlib
import cPickle as pickle
from bson.binary import Binary
from pymongo import MongoClient
from datetime import datetime, timedelta

from link_crawler import link_crawler


class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        """MongoDB缓存
        :param client: MongoDB数据库连接客户端
        :param expires: 设置过期时长
        """
        self.client = MongoClient('localhost', 27017) if client is None else client
        self.db = self.client.cache
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + ' dost not exist')

    def __setitem__(self, url, result):
        # record = {'result': result, 'timestamp': datetime.utcnow()}
        record = {'result': Binary(zlib.compress(pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)

    def clear(self):
        self.db.webpage.drop()


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/places/default/(index|view)', cache=MongoCache())
