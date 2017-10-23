#!/usr/bin/env python
# coding:utf-8

import csv
import string
import urllib
import urllib2
import cookielib
import lxml.html
import pytesseract
from PIL import Image
from io import BytesIO


REGISTER_URL = 'http://example.webscraping.com/places/default/user/register'


def parse_form(html):
    """从表单中找到所有的隐匿的input变量属性
    """
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def extract_image(html):
    """处理表单中嵌入的图片，解码之后保存img"""
    tree = lxml.html.fromstring(html)
    # 获取嵌入的图片数据
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')
    # remove data:image/png;base64, header
    img_data = img_data.partition(',')[-1]
    # open('test_.png', 'wb').write(data.decode('base64'))
    binary_img_data = img_data.decode('base64')
    file_like = BytesIO(binary_img_data)
    img = Image.open(file_like)
    # img.save('test.png')
    return img


def ocr(img):
    """使用开源的Tesseract OCR引擎对图片进行处理和识别
    pytesseract.image_to_string(Image.open('xxx.png'))
    """
    # 原始验证码图像 img = img.save('captcha_original.png')
    # 处理阈值图像忽略背景和文本, 灰度处理
    gray = img.convert('L')
    # 转换之后的灰度图 gray.save('captcha_greyscale.png')
    # 只有阀值小于1(全黑的颜色)的像素才能够保留下来
    bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    # 取阀值之后的图像 bw.save('captcha_threshold.png')
    word = pytesseract.image_to_string(bw)
    # 因为验证码重视小写, 我们进行消协处理, 增加识别率
    ascii_word = ''.join(c for c in word if c in string.letters).lower()
    return ascii_word


def register(first_name, last_name, email, password, captcha_fn):
    """实现自动注册
    :param first_name: 注册填写的名字
    :param last_name: 注册填写的姓氏
    :param email: 注册填写的邮箱
    :param password: 注册填写的密码
    :param captcha_fn: 识别验证码的函数
    :return: 是否登录成功
    """
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(REGISTER_URL).read()
    form = parse_form(html)
    form['first_name'] = first_name
    form['last_name'] = last_name
    form['email'] = email
    form['password'] = form['password_two'] = password
    img = extract_image(html)
    captcha = captcha_fn(img)
    form['recaptcha_response_field'] = captcha
    encoded_data = urllib.urlencode(form)
    request = urllib2.Request(REGISTER_URL, encoded_data)
    response = opener.open(request)
    success = '/user/register' not in response.geturl()
    return success


def test_samples():
    """测试精度的OCR图像样本
    """
    correct = total = 0
    for filename, text in csv.reader(open('samples/samples.csv')):
        img = Image.open('samples/' + filename)
        if ocr(img) == text:
            correct += 1
        total += 1
    print 'Accuracy: %d/%d' % (correct, total)


if __name__ == '__main__':
    print register(first_name='Test', last_name='Test', email='Test@webscraping.com', password='Test', captcha_fn=ocr)
