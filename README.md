# 网络爬虫指北攻略

![Author](https://img.shields.io/badge/Author-Escape-blue.svg)
![Build](https://img.shields.io/badge/Build-passing-brightgreen.svg)
![Languages](https://img.shields.io/badge/Languages-Python3.7-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)
![Contributions](https://img.shields.io/badge/Contributions-welcome-ff69b4.svg)


![index](./images/crawler-advance-guide.png)

## 1. 网络爬虫简介

> 理想情况下，网络爬虫并不是必需品，每个网站都应该提供`API`接口，以结构化的格式共享它们的数据。但是通常都会有限制，而且得到的数据有可能并不是我们期望得到的结果。

### 1.1 前期准备

`robots.txt`
- 建议爬虫的规范

`sitemap.xml`
- 检查网站地图，其中定义了网站的所以链接地址

估算网站大小
- 通过估算得到的数量来确定使用何种爬虫技术
- 通过浏览器的`site`参数估算网站的链接地址个数
- `site:example.webscraping.com/view`

识别网站所用的技术
- 通过`pip`安装第三方扩展`builtwith`来查询，`builtwith.parse('url')`

寻找网站所有者
- 通过`pip`安装第三方扩展`python-whois`来查询，`whois.whois('url')`


### 1.2 三种爬取方式

- 爬取网站地图
- 遍历每一个网页的数据库`ID`
- 追踪网页链接


### 1.3 高级特性

**(1)** 解析`robots.txt`
- `robotparser`模块中的`can_fetch`进行判断

**(2)** 支持代理
- `urllib2`模块
- `requests`模块

**(3)** 下载限速
- 时间戳记录访问时间，`time.sleep`进行限速

**(4)** 避免爬虫陷阱
- 记录深度，访问到当前网页经过了多少个链接



## 2. 数据抓取

> 抓取需求数据之前，需要我们对网页进行分析，利用浏览器的开发者工具对网页结构进行透彻的分析，这样可以方便我们后续爬取工作的进度。

### 2.1 网页抓取的方式

- 正则表达式
- `BeautifulSoup4`
- `Lxml`


### 2.2 `CSS`选择器

> 熟悉`jQuery`的一定很熟悉这样方式了

| 选择器 | 表示方式 |
| -------- | -------- |
| 选择所有标签 | `*` |
| 选择所有`<a>`标签 | `a` |
| 选择所有`class="link"`标签 | `.link` |
| 选择`class="link"`的`<a>`标签 | `a.link` |
| 选择`id="home"`的`<a>`标签 | `a#home` |
| 选择父元素为`<a>`标签的所有`<span>`子标签 | `a > span` |
| 选择`<a>`标签内部的所有`<span>`标签 | `a span` |
| 选择`title`属性为`"Home"`的所有`<a>`标签 | `a[title=Home]` |


### 2.3 性能对比

| 抓取方法 | 性能 | 使用难度 | 安装难度 |
| :-------- | :-------- | :------ | :------ |
| 正则表达式 | 快 | 困难 | 简单(内置模块) |
| `BeautifulSoup4` | 慢 | 简单 | 简单(纯Python) |
| `Lxml` | 快 | 简单 | 困难 |




## 3. 下载缓存

> 为了方便后续的使用以及资源的整合，我们需要对链接爬虫**添加缓存**的支持。当使用上缓存之后，就能够灵活的控制网页的爬虫质量。

### 3.1 磁盘缓存

**简述**

基于磁盘的缓存系统比较容易实现，无需安装其他模块，并且在文件管理器中就能查看结果。

避免这些限制的一种解决方案是使用 `URL` 的 哈希值作为文件名 。 尽管该方法可以带来一定改善 ，但是最终还是会面临许多文件系统具有的一个关键问题 ，那就是每个卷和每个目录下的文件数量是有限制 的 。如果缓存存储在`FAT32`文件系统中 ，每个目录的最大文件数是`65535` 。该限制可以通过将缓存分割到不同目录来避免 ，但是文件系统可存储 的文件总数也是有限制的 。我使用的`ext4`分区目前支持略多于`1500`万个文件，而一个大型网站往往拥有超过1亿个网页 。很遗憾 ，`DiskCache` 方法想要通用的话存在太多限制 。要想避免这些问题 ， 我们需要把多个缓存网页合并到一个文件中 ，并使用类似 `B＋`树的算法进行索引 。我们并不会自己实现这种算法 ，而是使用数据库缓存解决这个问题 。


### 3.2 数据库缓存

**NoSQL**
- `HBase`
 - 列数据存储
- `Redis`
 - 键值对存储
- `MongoDB`
 - 面向文档的数据库
- `Neo4j`
 - 图形数据库


**安装`MongoDB`**

```bash
# 安装MongoDb之后，在安装python的MongoDB封装库
$ pip install pymongo

# 启动本地MongoDB
$ mongod -dbpath .

# python连接MongoDB
>>> from pymongo import MongoClient
>>> client = MongoClient('localhost', 27017)
```


## 4. 并发下载

### 4.1 获取`URLS`链接地址

### 4.2 串行爬虫

### 4.3 多线程爬虫

### 4.4 多进程和多线程爬虫


## 5. 动态内容

> 和单页面应用的**简单表单事件**不同，使用`JavaScript`时，不再是加载后立即下载所有页面内容。这样就会造成许多网页在浏览器中展示的内容不会出现在`HTML`源代码中，本书前面介绍的抓取技术也就无法正常运转了 。所以这里我们采取两种方式进行抓取。
> - **`JavaScript`逆向工程**
> - **渲染`JavaScript`**

### 5.1 `AJAX`异步请求

> **`AJAX`**是指异步`JavaScript`和`XML`，描述了一种跨浏览器动态生成`Web`应用内容的功能。

1. 该技术允许`JavaScript`创建到远程服务器`HTTP`请求并获得响应，也就是说 `Web` 应用就可以传输和接收数据
2. 而传统的客户端与服务端交互方式则是刷新整个网页，这种方式的用户体验比较差，并且在只需传输少量数据时会造成带宽浪费。
3. 重要的实现函数为`XMLHttpRequest`方法。



### 5.2 `JavaScript`逆向工程

> **逆向工程: **该网页中的数据是使用 `JavaScript` 动态加载的，所以要想抓取该数据就需要了解网页是如何加载该数据的，该过程也被称为逆向工程。

**抓取方法**

- 在 `Firebug` 中单击 `Console` 选项卡，然后执行一次搜索，我们将会看到产生了一个请求信息。
- 请求的`URL`为`http://example.webscraping.com/places/ajax/search.json?&search_term=A&page_size=10&page=0`


#### 5.2.1 尝试匹配

- 由请求的`URL`可以知道参数为`search_term=`/`page_size=`/`page=`，对其进行匹配下载


#### 5.2.2 边界情况

- 对其参数边界的尝试，使分为多次的下载变为一次执行
- `search_term＝.`
- `page_size=1OOO`


### 5.3 渲染`JavaScript`

> 对于非常复杂的网站，我们很难实施逆向工程分析，及时使用了`Firebug`也很难进行理解。加之很多网站使用了`Google Web Toolkit(GWT)`技术进行开发，使得`JavaScript`代码是机器生成的压缩版。

- 我们可以使用**浏览器渲染引擎**避免这些工作，这种渲染引擎是浏览器在显示 网页时解析 `HTML`、应用 `css` 样式并执行 `JavaScript` 语句的部分 。
- 不同的浏览器有自己不同的渲染引擎，这里我们使用的`WebKit`。


#### 5.3.1 第三方库使用

- `Python`中解析渲染引擎的第三方库有`PyQt`/`PySide`等。


#### 5.3.2 `WebKit`与网站交互

> **交互：**实例类似于表单一样，将需要的信息动态的提交给网站。

- 实现`WebKit`爬虫最难得部分就是抓取搜索结果，因为很难预计结果的输出，所以这里我们有三种方式来处理这个问题。

**等待结果**

- 等待一定时间，期望`AJAX`事件能够在此时刻之前完成
 - **特点：**最易实现、效率低
- 重写`Qt`的网络管理器，跟踪`URL`请求的完成时间
 - **特点：**效率高、延迟出现在客户端则无法使用
- **轮询**网页等待特定内容出现
 - **特点：**更加可靠且易实现、检查内容是否加载完成时浪费`CPU`周期


**渲染类**

- 为了提升能后续的易用性，下面会把使用到的方法封装到一个类中。


### 5.4 Selenium

> 前面使用`WebKit`库，我们可以灵活的指定浏览器的渲染引擎。但是如果不需要这么完全控制所以行为的话，可以使用`Selenium`作为替代品，它提供了浏览器自动化的`API`接口。


### 5.5 总结

- 浏览器渲染引擎能够为我们节省了解网站后端工作原理的时间，但是该方法也有其劣势。
- 渲染网页增加了开销，使其比单纯下载 `HTML` 更慢。
- 另外，使用浏览器渲染引擎的方法通常需要轮询网页来检查是否已经得到事件生成的 `HTML` ，这种方式非常脆弱，在网络较慢时会经常会失败。
- 我一般将**浏览器渲染引擎作为短期解决方案**，此时长期的性能和可靠性并不算重要 ： 而作为**长期解决方案**需要尽最大努力对网站进行**逆向工程**。


## 6. 表单交互

> **表单交互：**用户与网页进行交互，根据用户的输入返回对应的内容。
> - 发送`POST`请求提交表单
> - 使用`cookie`登录网站
> - 用于简化表单提交的高级模块`Mechanize`

### 6.1 表单方法

- `GET`请求
 - 查询字符串
 - 提交的数据放在请求的`URL`中
 - `?name1=value1&name2=value2`
- `POST`请求
 - 提交的数据放在编码的请求体中
 - 避免暴露敏感数据在`URL`中



### 6.2 `cookie`和`session`

#### 6.2.1 `cookie`

**`cookie`的引入**

- 在程序中，**会话跟踪**是很重要的事情。理论上，一个用户的所有请求操作都应该属于同一个会话，而另一个用户的所有请求操作则应该属于另一个会话，二者不能混淆。

- 而`Web`应用程序是使用`HTTP`协议传输数据的。`HTTP`协议是**无状态**的协议。一旦数据交换完毕，客户端与服务器端的连接就会关闭，再次交换数据需要建立新的连接。这就意味着服务器无法从连接上**跟踪会话**。

- `Cookie`就是这样的一种机制。它可以弥补`HTTP`协议**无状态**的不足。在`Session`出现之前，基本上所有的网站都采用`Cookie`来**跟踪会话**。


**`cookie`的工作机制**

- 使用了`Cookie`之后，服务器通过给客户端**颁发通行证**的方式，就能够分辨出不同的用户。对应不同的用户携带自己通行证，服务端给出不同用户的信息数据。

- `Cookie`实际上是一小段的文本信息。客户端请求服务器，如果服务器需要记录该用户状态，就使用`response`向客户端浏览器颁发一个`Cookie`。客户端浏览器会把`Cookie`保存起来。当浏览器再请求该网站时，浏览器把请求的网址连同该`Cookie`一同提交给服务器。服务器检查该`Cookie`，以此来辨认用户状态。服务器还可以根据需要修改`Cookie`的内容。

**`Cookie`的特点**

- `Cookie`的有效期和域名
- `Cookie`的路径和安全属性
- `Cookie`的不可跨域名性
- `Unicode`编码保存中文
- `BASE64`编码保存二进制图片
- 浏览器不支持`Cookie`(手机)或`Cookie`被禁用，`Cookie`功能就失效

**用久登录的方法**

- 最直接的是把**用户名**与**密码**都保持到`Cookie`中，下次访问时检查`Cookie`中的用户名与密码，与数据库比较。这是一种**比较危险**的选择，一般不把密码等重要信息保存到`Cookie`中。
- 把**密码加密**后保存到`Cookie`中，下次访问时解密并与数据库比较。这种方案略微安全一些。如果不希望保存密码，还可以把登录的**时间戳**保存到`Cookie`与数据库中，到时只验证用户名与登录时间戳就可以了。


#### 6.2.2 `session`

**`session`引入**

- 除了使用`Cookie`，`Web`应用程序中还经常使用`Session`来记录客户端状态。**`Session`是服务器端使用的一种记录客户端状态的机制**，使用上比`Cookie`简单一些且更为安全，相应的也增加了服务器的存储压力。

**`session`机制**

- `Session`是另一种记录客户状态的机制，不同的是`Cookie`保存在**客户端**浏览器中，而`Session`保存在**服务器**上。客户端浏览器访问服务器的时候，服务器把客户端信息以某种形式记录在服务器上。这就是`Session`。客户端浏览器再次访问时只需要从该`Session`中查找该客户的状态就可以了。

- 如果说**`Cookie`机制**是通过检查客户身上的`“通行证”`来确定客户身份的话，那么**`Session`机制**就是通过检查服务器上的`“客户明细表”`来确认客户身份。`Session`相当于程序在服务器上建立的一份客户档案，客户来访的时候只需要查询客户档案表就可以了。

- `Session`保存在服务器端。为了获得更高的存取速度，服务器一般把`Session`放在内存里。每个用户都会有一个独立的`Session`。如果`Session`内容过于复杂，当大量客户访问服务器时可能会导致**内存溢出**。因此，`Session`里的信息应该**尽量精简**。

**`session`的要求**

- 虽然`Session`保存在服务器，对客户端是**透明的**，它的正常运行仍然需要客户端浏览器的支持。这是因为**`Session`需要使用`Cookie`作为识别标志**。

- `HTTP`协议是无状态的，`Session`不能依据`HTTP`连接来判断是否为同一客户，因此服务器向客户端浏览器发送一个名为`JSESSIONID`的`Cookie`，它的值为该`Session`的`id`。`Session`依据该`Cookie`来识别是否为同一用户。

- 因此同一机器的两个浏览器窗口访问服务器时，会生成两个不同的`Session`。但是由浏览器窗口内的链接、脚本等打开的新窗口（也就是说不是双击桌面浏览器图标等打开的窗口）除外。这类子窗口会共享父窗口的`Cookie`，因此会共享一个`Session`。

**`URL`地址重写**

- `URL`地址重写是对客户端不支持`Cookie`的解决方案。`URL`地址重写的原理是将该用户`Session`的`id`信息重写到`URL`地址中。服务器能够解析重写后的`URL`获取`Session`的`id`。这样即使客户端不支持`Cookie`，也可以使用`Session`来记录用户状态。

- 即在文件名的后面，在`URL`参数的前面添加了字符串`“;jsessionid=XXX”`。其中`XXX`为`Session`的`id`。分析一下可以知道，增添的`jsessionid`字符串既不会影响请求的文件名，也不会影响提交的地址栏参数。用户单击这个链接的时候会把`Session`的`id`通过`URL`提交到服务器上，服务器通过解析`URL`地址获得`Session`的`id`。

- 既然`wap(大部分手机端)`上大部分的客户浏览器都不支持`Cookie`，索性禁止`Session`使用`Cookie`，统一使用`URL`地址重写会更好一些。


#### 6.2.3 两者区别

| 特点 | `cookie` | `session` |
| ------ | ------ | ------ |
| **存放位置** | 客户浏览器 | 服务器 |
| **安全新** | 比较危险 | 比较安全 |
| **服务器性能** | 无影响 | 大量请求时会减轻服务性能 |
| **限制** | 单个`cookie`不允许超过`3k` | 基本无限制 |



### 6.3 登录表单

> 本章中我们还无法实现**全自动化注册表单**，因为涉及验证码的问题。

想要自动实现用户登录操作，需要使用开发者工具查看网站的`form`表单的格式和需要的信息。对其进行分析，之后尝试登录。

**图示表单组成**

- `action` => 设置表单数据提交的地址
 - 本例为`#`，表示和登录表单使用相同的`URL`地址
- `enctype` => 设置数据提交的编码
 - `POST`请求有两种编码类型
 - 普通文本内容使用`application/x-www-form-urlencoded`
 - 二进制流数据使用`multipart/form-data`
- `method` => 设置表单请求的方式
 - 本例为`POST`请求


**隐匿属性**

我们会注意到表单中还包含一部分隐藏起来的表单内容，如`name="_next"`/`name="_formkey"`/`name="_formname"`。这几个域对于表单提交来说很重要，使用代码提交的时候，如果没有则无法实现自动登录。

- `_formkey`
 - 服务器端使用这个唯一的`ID`来避免表单多次提交
 - 每次加载网页时都会产生不同的`ID`值
 - 服务器端通过这个给定的`ID`来判断表单是否已经提交过了
- `_formname`
 - 告诉服务端这个`ID`是`login`登录用的
- `_next`
 - 跳转之后的`URL`地址


**cookie**

当普通用户加载登录表单时，`_formkey`的值将会保存在`cookie`中，然后该值会与提交的登录表单数据中的`_formkey`进行对比，一致的话才能提交成功。

`cookie`的作用是让网站能够识别和跟踪用户。


### 6.4 从浏览器加载`cookie`

> 如何向服务器提交所需的登录信息有时很麻烦，我们使用一种变通的方式。即现在浏览器重手工执行登陆，然后在`Python`脚本中复用之前的得到的`cookie`，从而实现自动登录。
> - `Firofox`在`SQLite`中存放`cookie`，在`JSON`中存放`session`。


### 6.5 支持内容更新

> 支持内容更新的登录脚本扩展


### 6.6 `Mechanize`

> 使用`Mechanize`模块实现自动化表单处理


### 6.7 总结

在抓取网页时，和表单进行交互是一个非常重要的技能。 我们学习到了两种交互方法。

- 第一种是**分析表单**，然后手工生成期望的 `POST` 请求
- 第二种是直接使用高级模块 `Mechanize`


## 7. 验证码处理

> **验证码**(`APTCHA`)的全称为全自动区分计算机和人类的公开图灵测试，验证码用于测试用户是**否为真实人类**，比如许多银行网站强制每次登录时都需要输入验证码。

**自动化处理验证码**

- 首先使用光学字符识别`OCR`，将图片转化
- 然后使用一个验证码处理`API`，识别出验证码

**处理验证码的方法**

- 首先是使用`OCR`，然后是使用外部`API`。对于简单的验证码，或者需要处理大量验证码时，在`OCR`方法上花费时间是很值得的。否则，使用验证码处理`API`会更加经济有效。

-------------------

### 7.1 注册账号

> 在进行**账户注册**的时候，我们需要**填写表单**信息，并且需要识别验证码才能完成注册。要想完成**自动化注册**的功能，就需要让代码帮助我们**识别**网站的**验证码**。

- 因为每次加载表单时都会显示不同的验证码图像，所以为了了解表单需要哪些参数，我们可以复用上一章编写的 `parse form` 函数。

```python
#!/usr/bin/env python
# coding:utf-8

import pprint
import urllib2
import cookielib
import lxml.html

register_url = 'http://example.webscraping.com/places/default/user/register'


def parse_form(html):
    """从表单中找到所有的隐匿的input变量属性
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def register_args():
    """获取提交表单的所以参数
    """
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(register_url).read()
    form = parse_form(html)
    pprint.pprint(form)


if __name__ == '__main__':
    register_args()
```

- `recaptcha_response_field`是我们需要填写获取的验证码
- 其他的信息需要我们在注册的时候根据实际需求制定填写进去

```bash
{'_formkey': '799a82bf-4366-4b14-ba24-4e4800baa7ee',
 '_formname': 'register',
 '_next': '/places/default/index',
 'email': '',
 'first_name': '',
 'last_name': '',
 'password': '',
 'password_two': '',
 'recaptcha_response_field': None}
```

- 分析验证码图片之后，发现图片数据是**嵌入在网页中**的，而不是从其他的`URL`中加载过来的，所以我们使用**专门处理图片**的第三方库`Pillow`/`PIL`。

- 我们发现**图像数据**的**前缀**定义了**数据类型**，并且这是一张进行了 `Base64`编码的`PNG`图像，这种格式会使用`ASCII`编码表示**二进制数据**。

```html
<img src="data:image/png;base64,iVBO0...Ergg==&#10;">
```

- 我们可以通过在第一个逗号处分割的方法**移除该前缀**。然后，使用 `Base64` 解码图像数据，回到最初的**二进制格式** 。

- 要想加载图像，`PIL`需要一个类似文件的接口，所以在传给 `Image` 类之前，我们又使用了 `Bytes IO` 对这个二进制数据进行了**封装**。


-------------------

### 7.2 光学字符识别

- 最基本的方式
 - `image = Image.open("filename")`
- 类文件读取
 - `fp = open("filename", "rb"); im = Image.open(fp)`
- 字符串数据读取
 - `image = Image.open(StringIO.StringIO(buffer))`


-------------------

### 7.3 进一步改善

> 要想进一步改善验证码`OCR`的性能，下面还有些可能会使用到的方法。

- 实验不同阙值
- 腐蚀阙值文本，突出字符形状
- 调整图像大小（有时增大只寸会起到作用）
- 根据验证码字体训练`OCR`工具
- 限制结果为字典单词


## 8. Scrapy爬虫

### 8.1 Scrapy

#### 8.1.1 安装

- 安装`Scrapy`

```bash
$ pip install Scrapy
```

- 命令参数介绍

```bash
Usage:
  scrapy <command> [options] [args]

Available commands:
  startproject  创建新项目
  genspider    根据模板生成一个新的爬虫
  crawl        执行爬虫
  shell        启动交互式抓取控制台
  bench        快速运行基准测试
  fetch        获取一个URL使用Scrapy下载
  runspider    运行一个独立的爬虫(没有创建一个项目)
  settings      获取设置值
  version      打印Scrapy版本
  view          通过Scrapy在浏览器打开网址
```

-------------------

#### 8.1.2 启动项目

- 新建爬虫项目

```bash
$ scrapy startproject example
```

- 目录结构

```bash
$ tree example
example
├── example                # 项目名
│  ├── __init__.py
│  ├── items.py          # 定义了带抓区域的模型
│  ├── middlewares.py    # 
│  ├── pipelines.py      # 处理需要抓取的域
│  ├── settings.py        # 定义一些设置，如用户代理、抓取延时等
│  └── spiders            # 目录存储实际的爬虫代码
│      └── __init__.py
└── scrapy.cfg              # 项目配置
```

- `items.py`

```python
# -*- coding: utf-8 -*-

# 在这里定义爬虫的models需要获取的信息
# 可以参考 http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExampleItem(scrapy.Item):
    """ExampleItem类是一个模板, 需要将其中的内容替换为爬虫运行时想要存储的待抓取国家信息
    """
    name = scrapy.Field()
    population = scrapy.Field()
```

-------------------

#### 8.1.3 创建爬虫

- 生成初始模板

```python
# genspider: 根据模板生成一个新的爬虫
# country: 生成的爬虫文件名称
# example.webcraping.com: 爬取的域名地址
# crawl: 这里使用了内置的crawl模板

$ cd spiders
$ scrapy genspider country example.webcraping.com --template=crawl
```

- 生成的`country.py`

```python
# -*- coding: utf-8 -*-

# name: 定义爬虫名称
# allowed_domains: 定义可以抓取的域名列表, 没有定义表示任何域名
# start_urls: 爬虫起始的URL列表
# rules: 告诉爬虫需要跟踪哪些连接, 其中的callback函数用于解析下载的得到的响应
# 可以参考 http://doc.scrapy.org/en/latest/topics/spiders.html

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CountrySpider(CrawlSpider):
    name = 'country'
    allowed_domains = ['example.webcraping.com']
    start_urls = ['http://example.webcraping.com/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
```

-------------------

#### 8.1.4 优化设置

```python
# -*- coding: utf-8 -*-

# 爬虫example项目的设置文件
#
# 为了简单起见, 这个文件只包含设置考虑重要orcommonly使用, 你可以找到更多的设置咨询文档
#    http://doc.scrapy.org/en/latest/topics/settings.html
#    http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#    http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

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
#  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#  'Accept-Language': 'en',
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
```

-------------------

#### 8.1.5 测试爬虫

- 测试

```python
# 执行爬虫脚本crawl
# 指定输出信息级别LOG_LEVEL

$ scrapy crawl country -s LOG_LEVEL=ERROR
```

- 修改之后在爬取

```python
rules = (
    # follow: 表示爬取索引并跟踪其中的链接
    # callback: 表示抓取国家页面并下载响应传给callback函数处理
    Rule(LinkExtractor(allow=r'/index/'), callback='parse_item', follow=True),
    Rule(LinkExtractor(allow=r'/view/'), callback='parse_item')
)
```

```python
# 输出日志信息、索引页和国家页都可以正确爬取并已过滤了重复链接
# 但是发现爬虫浪费了很多资源爬取每个网页上的登录和注册表单链接

$ scrapy crawl country -s LOG_LEVEL=DEBUG
```

- 过滤地址

```python
rules = (
    # deny: 不需要处理的URL链接
    Rule(LinkExtractor(allow=r'/index/', deny='/user/'), callback='parse_item', follow=True),
    Rule(LinkExtractor(allow=r'/view/', deny='/user/'), callback='parse_item')
)
```

-------------------

#### 8.1.6 `Shell`命令抓取

- 使用`Shell`命令抓取

```python
$ scrapy shell http://example.webscraping.com/places/default/view/Afghanistan-1
```

```python
# 可以获取响应对象
In [1] response.url
In [2] response.status

# 使用lxml抓取数据
# 使用lxml选择器需要使用extract方法
In [3] name_css ＝ 'tr#places_country__row td.w2p_fw::text' 
In [4] response.css(name_css).extract()
```

- 完整版本`country.py`

```python
# -*- coding: utf-8 -*-

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from ..items import ExampleItem


class CountrySpider(CrawlSpider):
    name = 'country'
    allowed_domains = ['example.webscraping.com']
    start_urls = ['http://example.webscraping.com/']

    rules = (
        Rule(LinkExtractor(allow='/index/', deny='/user/'), follow=True),
        Rule(LinkExtractor(allow='/view/', deny='/user/'), callback='parse_item')
    )

    def parse_item(self, response):
        item = ExampleItem()
        item['name'] = response.css('tr#places_country__row td.w2p_fw::text').extract()
        item['population'] = response.css('tr#places_population__row td.w2p_fw::text').extract()
        return item
```

-------------------

#### 8.1.7 高级参数

- 文件导出

```bash
# output: 导出的文件名称

$ scrapy crawl country --output=countries.csv -s LOG_LEVEL=INFO
```

- 中断与恢复爬虫

```bash
# Scrapy内置了对暂停与恢复爬取的支持
# 我们只需要定义用于保存爬虫当前状态目录的JOBDIR设置即可
# 需要注意的是多个爬虫的状态需要保存在不同的目录当中

# 启动
$ scrapy crawl country -s LOG_LEVEL=DEBUG -s JOBDIR=crawls/country

# 中断
Ctrl+C

# 恢复
$ scrapy crawl country -s LOG_LEVEL=DEBUG - s JOBDIR=crawls/country
```

-------------------

### 8.2 Portia

> **`Portia`可视化爬虫：**是一款基于`Scrapy`开发的开源工具，该工具可以通过点击要抓取的网页部分来创建爬虫，这样就比手工创建`css`选择器的方式更加方便。

- `Portia`可视化爬虫

```python
https://github.com/scrapinghub/portia
```

- 使用`scrapely`实现自动化抓取

```python
https://github.com/scrapy/scrapely
```

**详情需要看文档**


## 实例说明

- 1.google_search.py
- 2.facebook_login.py
- 3.facebook_api.py
- 4.gap_market.py
- 5.bmw_map.py
- 6.html2pdf_lxf_git.py
