#!/usr/bin/env python
# coding:utf-8

"""
调用和风天气和百度语音API, 实现了自动播报当天天气的小工具
"""

import os
import json
import urllib2


class Weather:
    def __init__(self):
        self.CITY_ID = 'CN101110101'
        self.WEATHER_KEY = 'xxx'

    def weather_day(self):
        day_dict = {}
        weather_url = 'https://free-api.heweather.com/s6/weather/forecast?location={}&key={}'
        response = urllib2.urlopen(weather_url.format(self.CITY_ID, self.WEATHER_KEY)).read()
        json_response = json.loads(response)

        day_dict['status'] = json_response['HeWeather6'][0]['status']
        try:
            if day_dict['status'] != 'ok':
                return day_dict
        except Exception as e:
            print "ERROR:", e

        day_dict['location'] = json_response['HeWeather6'][0]['basic']['location']
        day_dict['local_time'] = json_response['HeWeather6'][0]['daily_forecast'][0]['date']
        day_dict['daytime'] = json_response['HeWeather6'][0]['daily_forecast'][0]['cond_txt_d']
        day_dict['evening'] = json_response['HeWeather6'][0]['daily_forecast'][0]['cond_txt_n']
        day_dict['wind_power'] = json_response['HeWeather6'][0]['daily_forecast'][0]['wind_sc']
        day_dict['temperature_min'] = json_response['HeWeather6'][0]['daily_forecast'][0]['tmp_min']
        day_dict['temperature_max'] = json_response['HeWeather6'][0]['daily_forecast'][0]['tmp_max']
        day_dict['visibility'] = json_response['HeWeather6'][0]['daily_forecast'][0]['vis']
        return day_dict

    def weather_now(self):
        now_dict = {}
        weather_url = 'https://free-api.heweather.com/s6/weather/now?location={}&key={}'
        response = urllib2.urlopen(weather_url.format(self.CITY_ID, self.WEATHER_KEY)).read()
        json_response = json.loads(response)

        now_dict['status'] = json_response['HeWeather6'][0]['status']
        try:
            if now_dict['status'] != 'ok':
                return now_dict
        except Exception as e:
            print "ERROR:", e

        now_dict['location'] = json_response['HeWeather6'][0]['basic']['location']
        now_dict['local_time'] = json_response['HeWeather6'][0]['update']['loc']
        now_dict['temperature'] = json_response['HeWeather6'][0]['now']['tmp']
        now_dict['current_weather'] = json_response['HeWeather6'][0]['now']['cond_txt']
        now_dict['wind_power'] = json_response['HeWeather6'][0]['now']['wind_sc']
        now_dict['visibility'] = json_response['HeWeather6'][0]['now']['vis']
        return now_dict

    def weather_life(self):
        life_dict = {}
        weather_url = 'https://free-api.heweather.com/s6/weather/lifestyle?location={}&key={}'
        response = urllib2.urlopen(weather_url.format(self.CITY_ID, self.WEATHER_KEY)).read()
        json_response = json.loads(response)

        life_dict['status'] = json_response['HeWeather6'][0]['status']
        try:
            if life_dict['status'] != 'ok':
                return life_dict
        except Exception as e:
            print "ERROR:", e

        life_dict['location'] = json_response['HeWeather6'][0]['basic']['location']
        life_dict['air_type'] = json_response['HeWeather6'][0]['lifestyle'][7]['type']
        life_dict['air_brf'] = json_response['HeWeather6'][0]['lifestyle'][7]['brf']
        life_dict['air_dec'] = json_response['HeWeather6'][0]['lifestyle'][7]['txt']
        return life_dict

    def weather_data(self):
        day = self.weather_day()
        life = self.weather_life()
        template = '{}日{}天气，白天天气{}，夜间天气{}，最高气温{}摄氏度，最低气温{}摄氏度，风力{}，能见度{}公里，空气质量{}，{}'
        data = template.format(day['local_time'].encode('utf-8'), day['location'].encode('utf-8'),
                               day['daytime'].encode('utf-8'), day['evening'].encode('utf-8'),
                               day['temperature_max'].encode('utf-8'), day['temperature_min'].encode('utf-8'),
                               day['wind_power'].encode('utf-8'), day['visibility'].encode('utf-8'),
                               life['air_brf'].encode('utf-8'), life['air_dec'].encode('utf-8'))
        return data


class SayWeather:
    def __init__(self):
        self.GRANT_TYPE = 'client_credentials'
        self.MAC_ADDRESS = 'xxx'
        self.CLIENT_ID = 'xxx'
        self.CLIENT_SECRET = 'xxx'
        self.VLC_APP = "/Applications/VLC.app/Contents/MacOS/VLC"

    def access_token(self):
        token_key_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type={}&client_id={}&client_secret={}'
        response = urllib2.urlopen(token_key_url.format(self.GRANT_TYPE, self.CLIENT_ID, self.CLIENT_SECRET)).read()
        json_response = json.loads(response)
        token_key = json_response['access_token']
        token_expires_time = json_response['expires_in']
        return token_key

    def say_weather(self):
        weather = Weather()
        tex = weather.weather_data()
        tok = self.access_token()
        url = "http://tsn.baidu.com/text2audio?tex=\'{}\'&tok=\'{}\'&cuid=\'{}\'&ctp=1&lan=zh&per=3"
        say_url = url.format(tex, tok, self.MAC_ADDRESS)
        os.system("{} {}".format(self.VLC_APP, say_url))


if __name__ == '__main__':
    say = SayWeather()
    say.say_weather()
