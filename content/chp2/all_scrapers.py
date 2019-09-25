import re
from bs4 import BeautifulSoup
from lxml.html import fromstring

from content.chp1.download import download

FIELDS = ('area', 'population', 'iso', 'country',
          'capital', 'continent', 'tld', 'currency_code',
          'currency_name', 'phone', 'postal_code_format', 'postal_code_regex',
          'languages', 'neighbours')


def re_scraper(html):
    """使用re正则表达式提取html文件中的国家信息"""
    results = []
    for field in FIELDS:
        results[field] = re.search(
            '<tr id="places_%s__row">.*?<td class="w2p_fw">(.*?)</td>' % field, html).groups()[0]
    return results

def bs_scraper(html):
    """使用bs4提取html文件中的国家信息"""
    soup = BeautifulSoup(html, 'html5lib')
    results = []
    for field in FIELDS:
        results[field] = soup.find(
            'table').find(
                'tr', id='places_%s__row' % field).find(
                    'td', class_='w2p_fw').text
    return results

def lxml_cssselect_scraper(html):
    """使用lxml的cssselect提取html文件中的国家信息"""
    tree = fromstring(html)
    results = []
    for field in FIELDS:
        results[field] = tree.cssselect(
            'table > tr#places_%s__row > td.w2p_fw' % field)[0].text_content()
    return results

def lxml_xpath_scraper(html):
    """使用lxml的xpath提取html文件中的国家信息"""
    tree = fromstring(html)
    results = []
    for field in FIELDS:
        results[field] = tree.xpath(
            '//tr[@id="places_%s__row"]/td[@class="w2p_fw"]' % field)[0].text_content()
    return results


if __name__ == '__name__':
    url = 'http://example.webscraping.com/view/UnitedKingdom-239'
    html = download(url)
    re_scraper(html)
    bs_scraper(html)
    lxml_cssselect_scraper(html)
    lxml_xpath_scraper(html)
