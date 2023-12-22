from hashlib import md5
import json
import random
import time
from typing import Any
import requests
import simple_cache
from core import config
from core.api import ApiException


class DtkClient():
    baseUrl = config.get("dtk.apiUrl")
    version = config.get("dtk.version")
    appKey =  config.get("dtk.appKey")
    appSerect = config.get("dtk.appSecret")
    
    
    def request(self, api, params,method='GET',fullUrl="",**kwargs):
        url = self.baseUrl + api
        if fullUrl is not None and fullUrl != "":
            url = fullUrl
        cache_file = "dtk.cache"

        uniqueStr = md5((method + url + json.dumps(params)).encode('utf-8')).hexdigest()
        cached =  simple_cache.load_key( cache_file,uniqueStr)
        if cached is not None:
            print("load from cache", cache_file, uniqueStr)
            return cached
        
        params =  self.sign(params)
        result =  requests.request(method, url, params=params,**kwargs)
        try:
            result = result.json()
        except Exception as e:
            raise Exception("返回不是 json 内容")
        simple_cache.save_key(cache_file, uniqueStr, result, 5 * 60)
        return result
    
    def get(self, api, params):
        return self.request(api, params, method='GET')
    
    def post(self, api, params):
        return self.request(api, params, method='POST')
    
    def sign(self, params):
        nonce = [random.randint(0, 9) for _ in range(6)]
        timer = int(time.time() * 1000)
        print("timerr",timer)
        appKey = self.appKey
        key = self.appSerect
        str = f'appKey={appKey}&timer={timer}&nonce={nonce}&key={key}'
        params['signRan'] =  md5(str.encode('utf-8')).hexdigest().upper()
        params['timer'] = timer
        params['nonce'] = nonce
        params['version'] = self.version
        params['appKey'] = self.appKey
        params['appSecret'] = self.appSerect
        return params
