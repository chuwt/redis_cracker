# coding: utf-8
"""
Created by chuwt on 18/4/3.
"""
# os

# third
import requests
# self


class ShodanAPI(object):
    def __init__(self):
        self.api_key = 'your api_key'
        self.base_url = 'https://api.shodan.io'

    def search(self):
        url = self.base_url + '/shodan/host/search'
        params = {
            'key': self.api_key,
            'query': 'port:6379',
            'page': 1
        }
        r = requests.get(url, params=params)


if __name__ == '__main__':
    s = ShodanAPI()
    s.search()

