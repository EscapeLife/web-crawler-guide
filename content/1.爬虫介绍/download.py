import re
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin

import requests


class Torottle:
    """爬取/抓取相同域名的网站设置延时时间"""
    def __init__(self, delay_time):
        self.delay_time = delay_time
        self.domains = {}
    
    def wait(self, url):
        domain = urljoin(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay_time > 0 and last_accessed is not None:
            sleep_secs = self.delay_time - (time.time() - last_accessed)
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = time.time()


class DownloadSite:
    """爬取/抓取获取对应网页的特定信息"""
    def __init__(self, url, num_retries=3, user_agent=None, proxies=None, robots_url=None):
        self.url = url
        self.num_retries = num_retries
        self.user_agent = user_agent
        self.proxies = proxies
        self.robots_url = robots_url

    def get_robots_parser(self):
        """获取对应robots.txt的文本信息"""
        rp = RobotFileParser()
        rp.set_url(self.robots_url)
        rp.read()
        return rp

    def download(self):
        """下载对应的HTML页面"""
        print(f'Downloading: {self.url} ...')
        headers = {'User-Agent': self.user_agent}
        try:
            resp = requests.get(self.url, headers=headers, params=self.proxies)
            html = resp.text
            if resp.status_code >= 400:
                print(f'Download Error: {self.url} => {self.num_retries} ...')
                html = None
                if self.num_retries and 500 <= resp.status_code < 600:
                    return self.download(self.url, self.num_retries-1)
        except requests.RequestException as e:
            print(f'Download Error: {e}')
            html = None
        return html        
