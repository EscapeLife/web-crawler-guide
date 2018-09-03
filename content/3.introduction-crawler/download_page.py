import requests


def download(method='GET', url=None, tries_num=2, user_agent=None):
    print('Download:', url)
    try:
        headers = {'User-Agent': user_agent}
        req = requests.request(method=method, url=url, headers=headers)
        print(req.headers)
        html = req.text
    except requests.Timeout as e:
        print('Download error:', e)
        html = None
        if tries_num > 0:
            print(req.status_code)
            if hasattr(req, 'status_code') and 500 < req.status_code < 600:
                return download(url, tries_num-1)
    finally:
        print(html)
        return html


download(url='http://httpstat.us/200', user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
