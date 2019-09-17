# I - 爬虫介绍

<p align=center>
  <a href="https://github.com/EscapeLife/DotFiles.git">
    <img src="https://github.com/EscapeLife/web-crawler-guide/blob/master/images/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB%E6%8C%87%E5%8C%97.png" >
  </a>
</p>

## 1. 思维脑图

<p align=center>
  <a href="https://github.com/EscapeLife/DotFiles.git">
    <img src="https://github.com/EscapeLife/web-crawler-guide/blob/master/images/%E7%88%AC%E8%99%AB%E5%85%A5%E9%97%A8-1.png" >
  </a>
</p>

## 2. 核心要点

<object data="https://github.com/EscapeLife/web-crawler-guide/blob/master/images/%E7%88%AC%E8%99%AB%E5%85%A5%E9%97%A8-2.pdf" width="700px" height="700px">
    <embed src="https://github.com/EscapeLife/web-crawler-guide/blob/master/images/%E7%88%AC%E8%99%AB%E5%85%A5%E9%97%A8-2.pdf">
        <p>This browser does not support SVG. Please download the SVG to view it: <a href="https://github.com/EscapeLife/web-crawler-guide/blob/master/images/%E7%88%AC%E8%99%AB%E5%85%A5%E9%97%A8-2.svg">Download SVG</a>.</p>
    </embed>
</object>

## 3. 代码说明

- **1. [download.py](https://github.com/EscapeLife/web-crawler-guide/blob/master/content/chp1/download.py)**
  - 包含下载网页以及解析robots.txt文件的函数
- **2. [throttle.py](https://github.com/EscapeLife/web-crawler-guide/blob/master/content/chp1/throttle.py)**
  - 包含相同域名的网页下载延迟设置
- **3. [web_crawler.py](https://github.com/EscapeLife/web-crawler-guide/blob/master/content/chp1/web_crawler.py)**
  - 包含网站地图爬虫、遍历ID爬虫、获取链接爬虫

## 4. 注意事项

- 写爬虫的时候，首先需要根据自己的目的以及收集到的信息来决定使用的技术和框架，其次就是由简及深的开始上手写爬虫，经过多次重构基本可以比较方便且灵活的使用了，最后就是需要写文档以及代码注释，以备日后查阅和翻看。
