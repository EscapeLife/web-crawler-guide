#!/usr/bin/env python
# coding:utf-8

# JavaScript渲染动态网页第三库使用实例说明

# 引入PyQt或者PySide库都可以，有少于差别
try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtWebKit import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    from PyQt4.QtWebKit import *

import lxml.html
import downloader


def direct_download(url):
    """下载网页源代码"""
    download = downloader.Downloader()
    return download(url)


def webkit_download(url):
    """第三方库渲染WebKit引擎"""
    # 框架首先创建QApplication对象实例
    app = QApplication([])
    # 创建Web文档的容器QWebView
    webview = QWebView()
    # loadFinished回调连接了QApplication的quit方法, 从而可以在网页加载完成之后停止事件循环
    webview.loadFinished.connect(app.quit)
    # 加载对于的JavaScript的URL地址
    webview.load(url)
    # 等待直到下载完成
    app.exec_()
    # 加载之后转换成HTML代码输出
    return webview.page().mainFrame().toHtml()


def parse(html):
    """使用lxml对得到的html源码解析"""
    tree = lxml.html.fromstring(html)
    print tree.cssselect('#result')[0].text_content()


def main():
    url = 'http://example.webscraping.com/dynamic'
    parse(direct_download(url))
    parse(webkit_download(url))
    return


if __name__ == '__main__':
    main()
