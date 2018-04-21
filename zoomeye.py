# coding: utf-8
"""
Created by chuwt on 18/4/3.
"""
# os
import json
import asyncio
import time
# third
import requests
import aiohttp
# self


class ZoomEye:
    def get_access_token(self):
        url = 'https://api.zoomeye.org/user/login'
        data = {
            "username": "your username",
            "password": "your password"
        }
        r = requests.post(url=url, data=json.dumps(data))
        access_token = (r.json()).get('access_token')
        return access_token

    # make it async
    def set_ip_to_file(self, token, page, _file):
        url = 'https://api.zoomeye.org/host/search?query=port:6379&page={}'.format(page)
        headers = {
            'Authorization': "JWT {}".format(token)
        }
        r = requests.get(url=url, headers=headers)
        matches = (r.json()).get('matches')
        if matches:
            for i in matches:
                ip = i.get('ip')
                portinfo = i.get('portinfo')
                key = portinfo.get('banner')
                if key.startswith('-NOAUTH Authentication required'):
                    continue
                if key.find('os:Windows') > 0:
                    continue
                else:
                    _file.write('{}\n'.format(ip))
                    _file.flush()

    def get_ips(self):
        token = self.get_access_token()
        with open('./ips.txt', 'a+') as f:
            for i in range(10000):
                print(i)
                self.set_ip_to_file(token, i, f)
                time.sleep(0.2)


if __name__ == '__main__':
    zoom = ZoomEye()
    zoom.get_ips()
