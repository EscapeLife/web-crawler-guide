#!/usr/bin/env python
# coding:utf-8

import re
import sys
import time
import urllib
import urllib2
from PIL import Image
from io import BytesIO

from form import register


def main(api_key, filename):
    captcha = CaptchaAPI(api_key)
    print register('Test Account', 'Test Account', 'example@webscraping.com', 'example', captcha.solve)


class CaptchaError(Exception):
    pass


class CaptchaAPI:
    def __init__(self, api_key, timeout=60):
        self.api_key = api_key
        self.timeout = timeout
        self.url = 'https://www.9kw.eu/index.cgi'

    def solve(self, img):
        """当准备好提交验证码并返回结果
        """
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_data = img_buffer.getvalue()
        captcha_id = self.send(img_data)
        start_time = time.time()
        while time.time() < start_time + self.timeout:
            try:
                text = self.get(captcha_id)
            except CaptchaError:
                pass # CAPTCHA still not ready
            else:
                if text != 'NO DATA':
                    if text == 'ERROR NO USER':
                        raise CaptchaError('Error: no user available to solve CAPTCHA')
                    else:
                        print 'CAPTCHA solved!'
                        return text
            print 'Waiting for CAPTCHA ...'
        raise CaptchaError('Error: API timeout')

    def send(self, img_data):
        """发送验证码来解决
        """
        print 'Submitting CAPTCHA'
        data = {
            'action': 'usercaptchaupload',
            'apikey': self.api_key,
            'file-upload-01': img_data.encode('base64'),
            'base64': '1',
            'selfsolve': '1',
            'maxtimeout': str(self.timeout)
        }
        encoded_data = urllib.urlencode(data)
        request = urllib2.Request(self.url, encoded_data)
        response = urllib2.urlopen(request)
        result = response.read()
        self.check(result)
        return result

    def get(self, captcha_id):
        """得到的结果解决验证码
        """
        data = {
            'action': 'usercaptchacorrectdata',
            'id': captcha_id,
            'apikey': self.api_key,
            'info': '1'
        }
        encoded_data = urllib.urlencode(data)
        response = urllib2.urlopen(self.url + '?' + encoded_data)
        result = response.read()
        self.check(result)
        return result

    def check(self, result):
        """检验结果的API和提高错误如果发现错误代码
        """
        if re.match('00\d\d \w+', result):
            raise CaptchaError('API error: ' + result)


if __name__ == '__main__':
    try:
        api_key = sys.argv[1]
        filename = sys.argv[2]
    except IndexError:
        print 'Usage: %s <API key> <Image filename>' % sys.argv[0]
    else:
        main(api_key, filename)
