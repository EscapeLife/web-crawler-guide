#!/usr/bin/env python
# coding:utf-8


import urllib
import urllib2
import pprint
import mechanize
import login

COUNTRY_URL = 'http://example.webscraping.com/edit/United-Kingdom-239'


# 网络机器人
def edit_country():
    """在登录情况下, 更新国家人口属性"""
    opener = login.login_cookies()
    country_html = opener.open(COUNTRY_URL).read()
    data = login.parse_form(country_html)
    pprint.pprint(data)
    print 'Population before: ' + data['population']
    data['population'] = int(data['population']) + 1
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(COUNTRY_URL, encoded_data)
    response = opener.open(request)

    country_html = opener.open(COUNTRY_URL).read()
    data = login.parse_form(country_html)
    print 'Population after:', data['population']


# Mechanize能够减轻表单的交互并提供很多高级接口
# 我们不需要再管理cookie信息了，可以更为容易的操作表单
# br.form可以直接获取提交之前的表单状态
# br.submit用于提交选定的登录表单
def mechanize_edit():
    """在登录情况下, 使用更新mechanize来国家人口属性
    """
    # 登录
    br = mechanize.Browser()
    br.open(login.LOGIN_URL)
    br.select_form(nr=0)
    print br.form
    br['email'] = login.LOGIN_EMAIL
    br['password'] = login.LOGIN_PASSWORD
    response = br.submit()

    # 更新国家人口属性
    br.open(COUNTRY_URL)
    br.select_form(nr=0)
    print 'Population before:', br['population']
    br['population'] = str(int(br['population']) + 1)
    br.submit()

    # 检测是否更新成功
    br.open(COUNTRY_URL)
    br.select_form(nr=0)
    print 'Population after:', br['population']


if __name__ == '__main__':
    edit_country()
    mechanize_edit()
