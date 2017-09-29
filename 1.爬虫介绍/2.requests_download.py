#!/usr/bin/env python
# coding:utf-8

import requests


def download(url, user_agent='smaller crawler', proxies=None, try_nums=2):
    print 'Downloading:', url
    if user_agent:
        headers = {user_agent: user_agent}
    else:
        headers = None
    if proxies:
        proxies = {proxies}

    try:
        r = requests.get(url, headers=headers, proxies=proxies)
        html = r.text
        code = r.status_code
        if try_nums > 0:
            if code is not None and 500 <= code < 600:
                html = download(url, user_agent, try_nums-1)
    except requests.HTTPError as e:
        print 'Error', e
    return html


if __name__ == '__main__':
    url = 'http://example.webscraping.com/places/default/index'
    download(url)
