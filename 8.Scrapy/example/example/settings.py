# -*- coding: utf-8 -*-

# 爬虫example项目的设置文件
#
# 为了简单起见, 这个文件只包含设置考虑重要orcommonly使用, 你可以找到更多的设置咨询文档
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'example'

SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'


# 用户代理
#USER_AGENT = 'example (+http://www.yourdomain.com)'

# 遵循robots.txt文件的规则
ROBOTSTXT_OBEY = True

# 配置由Scrapy最大并发请求, 默认同一个域名最多16个并发下载且没有延迟
#CONCURRENT_REQUESTS = 32

# 配置请求相同的网站的延迟时间, 默认值为0
# 更多参见 http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# 两次请求之间的延时
#DOWNLOAD_DELAY = 3
DOWNLOAD_DELAY = 3
# 下载延迟设置且只能设置一个值, 同一个域的延时或者同一个IP的延时
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
#CONCURRENT_REQUESTS_PER_IP = 16

# 禁用cookies, 默认为允许
#COOKIES_ENABLED = False

# 禁用Telnet远程登录, 默认为允许
#TELNETCONSOLE_ENABLED = False

# 覆盖默认的请求头
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# 启用或禁用蜘蛛中间件(middlewares)
# 更多参见 http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'example.middlewares.ExampleSpiderMiddleware': 543,
#}

# 启用或禁用下载中间件(middlewares)
# 更多参见 http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'example.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# 启用或禁用扩展
# 更多参见 http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# 配置item pipelines
# 更多参见 http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'example.pipelines.ExamplePipeline': 300,
#}

# 启用或禁用AutoThrottle扩展, 默认为禁用
# 更多参见 http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# 启用和配置HTTP缓存, 默认为禁用
# 更多参见 http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
