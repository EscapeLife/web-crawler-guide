#!/usr/bin/env python
# coding:utf-8

# 如果需要支持其他浏览器的cookie，可以使用第三方库browsercookie模块

import urllib
import urllib2
import glob
import sqlite3
import os
import cookielib
import json
import time
import lxml.html

LOGIN_EMAIL = 'example@webscraping.com'
LOGIN_PASSWORD = 'example'
LOGIN_URL = 'http://example.webscraping.com/places/default/user/login'


# 从浏览器获取cookie信息
def login_basic():
    """第一次登录失败并返回登录的URL地址, 因为没有使用到隐匿的_formkey
    """
    data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = urllib2.urlopen(request)
    print response.geturl()


def login_formkey():
    """第二次登录失败并返回登录的URL地址, 因为没有使用cookies对_formkey进行匹配
    """
    html = urllib2.urlopen(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = urllib2.urlopen(request)
    print response.geturl()


def login_cookies():
    """第三次登录成功返回登录页面的URL地址, 因为使用cookies和_formkey变量等
    """
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = opener.open(request)
    print response.geturl()
    return opener


def parse_form(html):
    """从表单中找到所有的隐匿的input变量属性
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


# 从浏览器加载cookie信息
def find_ff_sessions():
    """不同的操作系统存储session文件的位置不同，这里以firefox浏览器为例"""
    paths = [
        '~/.mozilla/firefox/*.default',
        '~/Library/Application Support/Firefox/Profiles/*.default',
        '%APPDATA%/Roaming/Mozilla/Firefox/Profiles/*.default'
    ]
    for path in paths:
        filename = os.path.join(path, 'sessionstore.js')
        matches = glob.glob(os.path.expanduser(filename))
        if matches:
            return matches[0]


def load_ff_sessions(session_filename):
    """把session解析到CookieJar对象
    """
    cj = cookielib.CookieJar()
    if os.path.exists(session_filename):
        try:
            json_data = json.loads(open(session_filename, 'rb').read())
        except ValueError as e:
            print 'Error parsing session JSON:', str(e)
        else:
            for window in json_data.get('windows', []):
                for cookie in window.get('cookies', []):
                    import pprint
                    pprint.pprint(cookie)
                    c = cookielib.Cookie(0,
                                         cookie.get('name', ''),
                                         cookie.get('value', ''), None, False,
                                         cookie.get('host', ''),
                                         cookie.get('host', '').startswith('.'),
                                         cookie.get('host', '').startswith('.'),
                                         cookie.get('path', ''), False, False,
                                         str(int(time.time()) + 3600 * 24 * 7), False,
                                         None, None, {})
                    cj.set_cookie(c)
    else:
        print 'Session filename does not exist:', session_filename
    return cj


def login_firefox():
    """从firefox加载cookies信息
    """
    session_filename = find_ff_sessions()
    cj = load_ff_sessions(session_filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # COUNTRY_URL为登录之后的URL地址
    html = opener.open(COUNTRY_URL).read()

    # 这里无法再依靠登录跳转了，只能抓取登录产生的HTML代码进行检测，这里获得登录成功的欢迎信息
    tree = lxml.html.fromstring(html)
    print tree.cssselect('ul#navbar li a')[0].text_content()
    return opener


def main():
    login_cookies()


if __name__ == '__main__':
    main()
