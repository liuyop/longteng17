"""请求方法的封装"""
import requests
import json

TIMEOUT = 30 #默认超时时间


class Api(object):
    def __init__(self, base_url=None):
        self.session = requests.session()
        self.base_url = base_url
        # self.login()

    def request(self, method, url, **kwargs):
        url = self.base_url + url if self.base_url else url
        kwargs['timeout'] = kwargs.get('timeout', TIMEOUT) #从字典中获取用户传过来的默认超时时间，没有则取TIMEOUT默认值
        print(f"请求数据: {method} {url} {kwargs}")
        res = self.session.request(method, url, **kwargs)
        print(f"响应数据: {res.text}")
        return res

    def get(self, url, **kwargs):
        return self.request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('post', url, **kwargs)

    def login(self):
        pass
