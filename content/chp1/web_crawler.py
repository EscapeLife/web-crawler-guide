import itertools
import re
from urllib.parse import urljoin

from content.chp1.download import download, get_robots_parser
from content.chp1.throttle import Throttle


def crawl_sitemap(url):
    """
    1.站点地图爬虫
    http://example.python-scraping.com/view/11.网站地图爬虫
    http://example.python-scraping.com/sitemap.xml
    """
    sitemap = download(url)
    page_links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in page_links:
        html = download(link)


def crawl_id(url, max_errors=5):
    """
    2.ID遍历爬虫
    http://example.python-scraping.com/view/
    """
    num_error = 0
    for page_id in itertools.count(1):
        page_url = f'{url}{page_id}'
        html = download(page_url)
        if html in None:
            num_error += 1
            if num_error == max_errors:
                break
        else:
            num_error = 0


def crawl_link(start_url, link_regex, robots_url=None, user_agent=None,
               proxies=None, delay_time=5, max_depth=4):
    """
    3.链接爬虫
    只需将max_depth设为一个负数即可当前深度永远不会与之相等
    http://example.python-scraping.com/view/1
        > (1)解析robots.txt文件
        > (2)支持代理
        > (3)下载限速
        > (4)避免爬虫陷阱
    """
    crawl_queue = [start_url]
    seen_links_dict = {}
    throttle = Throttle(delay_time)
    if not robots_url:
        robots_url = f'{start_url}/robots.txt'
    rp = get_robots_parser(robots_url)

    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch(user_agent, url):
            depth = seen_links_dict(url, 0)
            if depth == max_depth:
                print(f'Skipping {url} due to depth ...')
                continue
            throttle.wait(url)
            html = download(url, user_agent=user_agent, proxies=proxies)
            if not html:
                continue
            for link in get_links(html):
                if re.match(link_regex, link):
                    abs_link = urljoin(start_url, link)
                    if abs_link not in seen_links_dict:
                        seen_links_dict[abs_link] = depth + 1
                        crawl_queue.append(abs_link)
        else:
            print(f'Blocked by robots.txt {url} ...')


def get_links(html):
    """返回正则表达式匹配的链接地址内容"""
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    return webpage_regex.findall(html)
