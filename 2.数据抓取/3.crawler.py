#!/usr/bin/env python
# coding:utf-8

import re
import csv
import time
import Queue
import urllib2
import urlparse
import lxml.html
import robotparser
from datetime import datetime


def link_crawler(seed_url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, user_agent='wswp', proxy=None, num_retries=1, scrape_callback=None):
    """追踪链接爬虫
    :param seed_url: 爬虫入口地址
    :param link_regex: 匹配正则过滤
    :param delay: 下载显示时间
    :param max_depth: 最大深度
    :param max_urls: 下载总数
    :param headers: 设置头信息
    :param user_agent: user_agent参数
    :param proxy: 设置代理
    :param num_retries: 重新下载次数
    :param scrape_callback: 回调类
    :return: 网站源代码信息
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
            # 提取网页内容保存在CSV文件中
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])

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


class ScrapeCallback:
    """回调类
    __call__方法是一个特殊的方法，在对象作为函数被调用时会调用该方法
    scrape_callback(url, html) 等价于 scrape_callback.__call__(url, html)
    """
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = lxml.html.fromstring(html)
            row = []
            for field in self.fields:
                row.append(tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))[0].text_content())
            self.writer.writerow(row)


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com', '/places/default/(index|view)', scrape_callback=ScrapeCallback())
