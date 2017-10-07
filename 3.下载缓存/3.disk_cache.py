#!/usr/bin/env python
# coding:utf-8

import os
import re
import zlib
import shutil
import urlparse
import cPickle as pickle
from datetime import datetime, timedelta

from link_crawler import link_crawler


class DiskCache:
    """通过使用磁盘空间保存文件的方式对资源文件进行缓存
    """
    def __init__(self, cache_dir='cache', expires=timedelta(days=30), compress=True):
        """设置代码保存的磁盘位置、设置文件过期时长、设置是否对文件进行压缩
        """
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    def __getitem__(self, url):
        """从磁盘加载数据的URL
        """
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """这个URL保存数据到磁盘
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        data = pickle.dumps((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __delitem__(self, url):
        """删除这个关键的价值和任何空的子目录
        """
        path = self.url_to_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    def url_to_path(self, url):
        """为这个URL创建文件系统路径
        """
        components = urlparse.urlsplit(url)
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    def has_expired(self, timestamp):
        """返回这个时间戳是否已经过期
        """
        return datetime.utcnow() > timestamp + self.expires

    def clear(self):
        """清除所有缓存的值
        """
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/places/default/(index|view)', cache=DiskCache())
