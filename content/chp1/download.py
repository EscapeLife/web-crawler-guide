from urllib import robotparser
import requests


def download(url, num_tries=3, user_agent=None, proxies=None):
    """下载给定的URL并返回页面内容"""
    print(f'Download: {url} ...')
    headers = {'User-Agent': user_agent}
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text
        if resp.status_code >= 400:
            print(f'Download Error: {url} => {num_tries} ...')
            html = None
            if num_tries and 500 <= resp.status_code < 600:
                return download(url, num_tries-1)
    except requests.RequestException as e:
        print(f'Download Error: {e} ...')
        html = None
    return html


def get_robots_parser(robots_url):
    """返回robots.txt文件的解析信息
    http://example.python-scraping.com/robots.txt
    """
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp
