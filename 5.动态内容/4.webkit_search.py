#!/usr/bin/env python
# coding:utf-8

# 实现网站搜索页面的动态获取

try:
    from PySide.QtGui import QApplication
    from PySide.QtCore import QUrl, QEventLoop, QTimer
    from PySide.QtWebKit import QWebView
except ImportError:
    from PyQt4.QtGui import QApplication
    from PyQt4.QtCore import QUrl, QEventLoop, QTimer
    from PyQt4.QtWebKit import QWebView


def main():
    app = QApplication([])
    webview = QWebView()
    # 创建QEventLoop对象, 该对象用于创建本地事件循环
    loop = QEventLoop()
    webview.loadFinished.connect(loop.quit)
    webview.load(QUrl('http://example.webscraping.com/search'))
    # 由于QWebView是异步加载的, 但我们希望等待网页加载完成, 因此需要在事件循环启动时调用loop.exec()方法
    loop.exec_()

    # 调用QWebView GUI的show()方法来显示渲染窗口和便于调试
    webview.show()
    # 渲染窗口进行封装且QWebFrame类有很多与网页交互的有用方法
    frame = webview.page().mainFrame()
    # 网页中input的输入框id为search_term
    frame.findFirstElement('#search_term').setAttribute('value', '.')
    # 网页中选项卡id为page_size
    frame.findFirstElement('#page_size option:checked').setPlainText('1000')
    # evaluateJavaScript可以指定我们需要调用的js代码, 这里进行了表单的提交操作
    frame.findFirstElement('#search').evaluateJavaScript('this.click()')

    elements = None
    while not elements:
        app.processEvents()
        # 使用了第三种方法来获得相应的网页
        elements = frame.findAllElements('#results a')
    countries = [e.toPlainText().strip() for e in elements]
    print countries


if __name__ == '__main__':
    main()
