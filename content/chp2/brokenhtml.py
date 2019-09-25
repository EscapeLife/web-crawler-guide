from bs4 import BeautifulSoup
from lxml.html import fromstring, tostring

broken_html = '<ul class=country><li>Area<li>Population</ul>'


def bs_brokenhtml():
    """使用BeautifulSoup补全缺失的html文件"""
    soup = BeautifulSoup(broken_html, 'html.parser')
    fixed_html = soup.prettify()
    print(f'the bs4 fixed html: {fixed_html}')

    ul = soup.find('ul', attrs={'class': 'country'})
    print(f'the first match: {ul.find("li")}')
    print(f'the all matches: {ul.find_all("li")}')

def lxml_brokenhtml():
    """使用lxml补全缺失的html文件"""
    tree = fromstring(broken_html)
    fixed_html = tostring(tree, pretty_print=True)
    print(f'the lxml fixed html: {fixed_html}')

    ul = tree.cssselect('ul.country')[0]
    print(f'{ul.text_content()}')

if __name__ == '__main__':
    bs_brokenhtml()
    lxml_brokenhtml()
