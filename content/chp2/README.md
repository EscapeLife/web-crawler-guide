# II - 数据爬取

> **在上一章中，我们构建跟踪链接的爬虫来下载所需的网页。虽然有意思却不够实用，因为爬下来的网页都被丢弃了。现在，我们需要然它干点事情了。**

<p align=center>
  <a href="https://github.com/EscapeLife/DotFiles.git">
    <img src="https://github.com/EscapeLife/web-crawler-guide/blob/master/images/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB%E6%8C%87%E5%8C%97.png" >
  </a>
</p>


## 1. 思维脑图

![数据爬取]()


## 2. 核心要点

**1.简单的re正则表达式**

- 正则表达式为我们提供了抓取数据的快捷方式，但是该方法过于脆弱，容易在网页更新后出现问题，导致爬虫无法抓取到正确的内容。

**2.流行的BeautifulSoup模块**

- **使用html5lib解析器:** `soup = BeautifulSoup(html, 'html5lib')`(效果好)
- **使用html.parser解析器:** `soup = BeautifulSoup(html, 'html.parser')`
- 我们知道即使页面中包含了不完整的HTML内容，使用BeautifulSoup模块也能帮助我们整理该页面，从而让我们可以从非常不完整的网站代码中抽取数据。

**3.强大的lxml模块**

- **使用XPath选择器:** `pip install lxml`(默认)
- **使用cssselect选择器:** `pip install cssselect`
- Lxml是基于libxml2这一XML解析库构建的Python库，它使用C语言编写，解析速度比BeautifulSoup更快，不过安装过程也更为复杂。

| 选择器描述 | XPath选择器 | CSS选择器 |
| -------- | ---------- | -------- |
| 选择所有链接 | `'//a'` | `'a'` |
| 选择类名为"main"的 div 元素 | `'//div[@class="main"]'` | `'div.main'` |
| 选择ID为"list"的ul元素 | `'//ul[@id="list"]'` | `'ul#list'` |
| 从所有段落中选择文本 | `'//p/text()'` | `'p'*` |
| 选择所有类名中包含'test'的div元素 | `'//div[contains(@class, 'test')]'` | `'div [class*="test"]'` |
| 选择所有包含链接或列表的div元素 | `'//div[a\|ul]'` | `'div a, div ul'` |
| 选择href属性中包含google的链接 | `'//a[contains(@href, "google")]` | `'a'*` |

**4.LXML和家族树**

- lxml同样也有遍历HTML页面中家族树的能力，希望查找页面中同一节点深度的所有元素时就需要查找它们的兄弟，或是希望得到页面中某个特定元素的所有子元素时。结合XPath表达式遍历家族关系是一个能够让你不丢失任何内容的好方式，即使该元素没有可识别的CSS选择器，该方法同样也可以工作。
- 虽然我们强烈鼓励使用lxml进行解析，不过网络抓取的最大性能瓶颈通常是网络。我们将会讨论并行工作流的方法，从而让你能够通过并行处理多个请求工作，来提升爬虫的速度。

**5.抓取总结**

- 如果对你来说速度不是问题，并且更希望只使用pip安装库的话，那么使用较慢的方法(如BeautifulSoup)也不成问题。如果只需抓取少量数据，并且想要避免额外依赖的话，那么正则表达式可能更加适合。不过，通常情况下，lxml是抓取数据的最佳选择，这是因为该方法既快速又健壮，而正则表达式和BeautifulSoup或是速度不快，或是修改不易。

| 抓取方法 | 性能 | 使用难度 | 安装难度|
| ----- | ----- | ----- | ----- |
| 正则表达式 | 快 | 困难 | 简单(内置模块) |
| BeautifulSoup | 慢 | 简单 | 简单(纯Python) |
| Lxml | 快 | 简单 | 相对困难 |


## 3. 代码说明

- 

## 4. 注意事项

**XPath选择器**

- 有时候使用CSS选择器无法正常工作，尤其是在HTML非常不完整或存在格式不当的元素时。尽管像BeautifulSoup和lxml这样的库已经尽了最大努力来纠正解析并清理代码，然而它可能还是无法工作，在这些情况下，XPath可以帮助你**基于页面中的层次结构关系构建**非常明确的选择器。XPath是一种将XML文档的层次结构描述为关系的方式。因为HTML是由XML元素组成的，因此我们也可以使用XPath从HTML文档中定位和选择元素。