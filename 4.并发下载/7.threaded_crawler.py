#!/usr/bin/env python
# coding:utf-8

import time
import threading
import urlparse

from downloader import Downloader

SLEEP_TIME = 1


def normalize(seed_url, link):
    """正常化这个URL通过删除哈希和添加域
    """
    link, _ = urlparse.urldefrag(link)
    return urlparse.urljoin(seed_url, link)


def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None,
                     num_retries=1, max_threads=10, timeout=60):
    """多线程下载
    :param seed_url: 入口url地址
    :param delay: 设置同域下载延时
    :param cache: 设置缓存模型
    :param scrape_callback: 获取urls
    :param user_agent: 设置user_agent头
    :param proxies: 设置代理
    :param num_retries: 设置下载重试次数
    :param max_threads: 设置多线程个数
    :param timeout: 设置超时时间
    :return: None
    """
    crawl_quene = [seed_url]
    seen = set([seed_url])
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, timeout=timeout)

    def process_queue():
        while True:
            try:
                url = crawl_quene.pop()
            except IndexError:
                break
            else:
                html = D(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        print 'Error in callback for: {}: {}'.format(url, e)
                    else:
                        for link in links:
                            link = normalize(seed_url, link)
                            if link not in seen:
                                seen.add(link)
                                crawl_quene.append(link)

        threads = []
        while threads or crawl_quene:
            for thread in threads:
                if not thread.is_alive():
                    # 删除停止线程
                    threads.remove(thread)
            while len(threads) < max_threads and crawl_quene:
                thread = threading.Thread(target=process_queue)
                # 守护进程的主线程可以设置退出时接收ctrl-c
                thread.setDaemon(True)
                thread.start()
                threads.append(thread)
            time.sleep(SLEEP_TIME)
