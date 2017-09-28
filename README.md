# 网络爬虫


## 1. 网络爬虫简介

> 理想情况下，网络爬虫并不是必需品，每个网站都应该提供`API`接口，以结构化的格式共享它们的数据。但是通常都会有限制，而且得到的数据有可能并不是我们期望得到的结果。

### 1.1 前期准备

- `robots.txt`
 - 建议爬虫的规范
- `sitemap.xml`
 - 检查网站地图，其中定义了网站的所以链接地址
- 估算网站大小
 - 通过估算得到的数量来确定使用何种爬虫技术
 - 通过浏览器的`site`参数估算网站的链接地址个数
 - `site:example.webscraping.com/view`
- 识别网站所用的技术
 - 通过`pip`安装第三方扩展`builtwith`来查询，`builtwith.parse('url')`
- 寻找网站所有者
 - 通过`pip`安装第三方扩展`python-whois`来查询，`whois.whois('url')`


### 1.2 三种爬取方式

- 爬取网站地图
- 遍历每一个网页的数据库`ID`
- 追踪网页链接


### 1.3 爬取方式实例

```python
#!/usr/bin/env python
# coding:utf-8

import re
import urllib2
import urlparse
import itertools
import time


def download(url, user_agent='wswp', try_nums=2):
    """
    下载函数
    :param url: 网站地址
    :param user_agent: 设置用户代理
    :param try_nums: 设置重试次数
    :return: 网站页面源代码
    """
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
        time.sleep(2)
    except urllib2.URLError as e:
        print 'Download Error:', e.reason
        html = ''
        if try_nums > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                return download(url, user_agent, try_nums-1)
    return html


def crawl_sitemap(url):
    """
    网站地图爬虫
    :param url: 网站地址
    :return: 网站页面源代码
    """
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:
        html = download(link)
        return html


def crawl_db_number(max_errors=5, num_errors=0):
    """
    遍历数据库ID爬虫
    :param max_errors: 最大容错次数
    :param num_errors: 错误统计次数
    :return: 网站页面源代码
    """
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/places/default/view/%d' % page
        html = download(url)
        if html is None:
            num_errors += 1
            if num_errors == max_errors:
                break
            else:
                num_errors = 0


def link_crawler(seed_url, link_regex):
    """
    追踪链接爬虫
    :param seed_url: 爬取的网站地址
    :param link_regex: 追踪链接的正则表达式
    :return:
    """
    crawl_queue = [seed_url]
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_link(html):
            if re.match(link_regex, link):
                link = urlparse.urljoin(seed_url, link)
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)


def get_link(html):
    """
    返回HTML文件中的所有a标签的链接地址列表
    :param html: 追踪的HTML文件
    :return: 所有a标签的链接地址列表
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)
```


### 1.4 高级特性

- **(1)** 解析`robots.txt`
 - `robotparser`模块中的`can_fetch`进行判断
- **(2)** 支持代理
 - `urllib2`模块
 - `requests`模块
- **(3)** 下载限速
 - 时间戳记录访问时间，`time.sleep`进行限速
- **(4)** 避免爬虫陷阱
 - 记录深度，访问到当前网页经过了多少个链接

```python
import re
import urlparse
import urllib2
import time
import robotparser
import Queue
from datetime import datetime


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1):
    """追踪链接爬虫
    """
    # 获取需要抓取的URL链接地址
    crawl_queue = Queue.deque([seed_url])
    # 访问过的URL链接以及深度
    seen = {seed_url: 0}
    # 追踪有多少URL被下载
    num_urls = 0
    # 下载速度限制
    throttle = Throttle(delay)

    # 解析robots.txt文件
    rp = get_robots(seed_url)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_queue:
        url = crawl_queue.pop()
        # 检测url是否被robots.txt文件限制
        if rp.can_fetch(user_agent, url):
            throttle.wait(url)
            html = download(url, headers, proxy=proxy, num_retries=num_retries)
            links = []

            depth = seen[url]
            if depth != max_depth:
                if link_regex:
                    links.extend(link for link in get_links(html) if re.match(link_regex, link))

                for link in links:
                    link = normalize(seed_url, link)
                    # 检测是否已经爬取过这个链接
                    if link not in seen:
                        seen[link] = depth + 1
                        # 检测两个链接是否是相同的域, 不爬取非本站点的连接
                        if same_domain(seed_url, link):
                            crawl_queue.append(link)

            # 检查是否已达到最大下载
            num_urls += 1
            if num_urls == max_urls:
                break
        else:
            print 'Blocked by robots.txt:', url


class Throttle:
    """通过对比时间戳的方式，进行下载速度限制
    """
    def __init__(self, delay):
        # 限制时间
        self.delay = delay
        # 访问时间戳
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


def download(url, headers, proxy, num_retries, data=None):
    """网页下载函数
    """
    print 'Downloading:', url
    request = urllib2.Request(url, data, headers)

    # 设置代理
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))

    try:
        response = opener.open(request)
        html = response.read()
        code = response.code
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if num_retries > 0 and 500 <= code < 600:
                return download(url, headers, proxy, num_retries - 1, data)
        else:
            code = None
    return html


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link)  # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """检测两个链接是否是相同的域, 不爬取非本站点的连接
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def get_robots(url):
    """站点初始化robots parser
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def get_links(html):
    """返回HTML文件中的a标签列表
    """
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)
```
