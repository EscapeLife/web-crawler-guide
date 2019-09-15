import time
from urllib.parse import urlparse


class Throttle:
    """下载同一域名下的内容设置时间延迟"""
    def __init__(self, delay_time):
        self.delay_time = delay_time
        self.domains = {}

    def wait(self, url):
        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay_time > 0 and last_accessed is not None:
            sleep_secs = self.delay_time - (time.time() - last_accessed)
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = time.time()
