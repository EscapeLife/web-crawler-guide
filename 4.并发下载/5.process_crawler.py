#!/usr/bin/env python
# coding:utf-8

import time
import urlparse
import threading
import multiprocessing

from mongo_cache import MongoCache
from mongo_queue import MongoQueue
from downloader import Downloader

SLEEP_TIME = 1


def normalize(seed_url, link):
    """正常化这个URL通过删除哈希和添加域
    """
    link, _ = urlparse.urldefrag(link)
    return urlparse.urljoin(seed_url, link)


def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None, num_retries=1, max_threads=10, timeout=60):
    """多线程下载
    """
    # crawl_queue定义URL的队列需要爬取下载的地址
    crawl_queue = MongoQueue()
    crawl_queue.clear()
    crawl_queue.push(seed_url)
    D = Downloader(cache=cache, delay=delay, user_agent=user_agent, proxies=proxies, num_retries=num_retries, timeout=timeout)

    def process_queue():
        while True:
            # 跟踪处理url
            try:
                url = crawl_queue.pop()
            except KeyError:
                # 当前没有urls进程
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
                            # 向queue添加新的link
                            crawl_queue.push(normalize(seed_url, link))
                crawl_queue.complete(url)

    # 等待所有下载线程完成
    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue.peek():
            thread = threading.Thread(target=process_queue)
            # 守护进程的主线程可以设置退出时接收ctrl-c
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)


def process_crawler(args, **kwargs):
    """多进程下载
    """
    num_cpus = multiprocessing.cpu_count()
    # pool = multiprocessing.Pool(processes=num_cpus)
    print 'Starting {} processes'.format(num_cpus)
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=[args], kwargs=kwargs)
        # parsed = pool.apply_async(threaded_link_crawler, args, kwargs)
        p.start()
        processes.append(p)
    # 等待进程完成
    for p in processes:
        p.join()
