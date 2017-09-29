#!/usr/bin/env python
# coding:utf-8

import re
import urllib2
import lxml.html
from bs4 import BeautifulSoup


def download(url, user_agent=None):
    """下载网页源码
    """
    print 'Downloading:', url
    headers = {'User-agent': user_agent or 'wswp'}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
    return html


def re_crawler(url):
    """正则表达式进行数据抓取
    正则表达式提供了一种数据抓取的快捷方式，但是方法过于脆弱而无法满足未来
    """
    html = download(url)
    # print re.findall('<td class="w2p_fw">(.*?)</td>', html)
    print re.findall('<tr id="places_area__row">.*?<td\s*class="w2p_fw">(.*?)</td>', html)


def bs_crawler(url):
    """使用BeautifulSoup对HTML进行解构，提取有用的数据
    """
    html = download(url)
    soup = BeautifulSoup(html, "html.parser")
    # tr = soup.find(attrs={'id': 'places_area__row'})
    # td = tr.find(attrs={'class': 'w2p_fw'})
    # print td.text
    tr = soup.find('tr', id='places_area__row')
    td = tr.find('td', class_='w2p_fw')
    return td.get_text()


def lxml_crawler(url):
    html = download(url)
    tree = lxml.html.fromstring(html)
    td = tree.cssselect('tr#places_neighbours__row > td.w2p_fw')[0]
    return td.text_content()


if __name__ == '__main__':
    url = 'http://example.webscraping.com/places/default/view/239'
    bs_crawler(url)

