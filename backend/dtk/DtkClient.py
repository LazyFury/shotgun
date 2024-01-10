from hashlib import md5
import json
import random
import time
import requests
import simple_cache
from backend import settings
from core import config


class DtkClient():
    baseUrl = config.get("dtk.apiUrl")
    version = config.get("dtk.version")
    appKey =  config.get("dtk.appKey")
    appSerect = config.get("dtk.appSecret")
    cache_file = config.cacheFile("dtk.cache")
    
    
    def request(self, api, params,method='GET',fullUrl="",cache=5,**kwargs):
        url = self.baseUrl + api
        if fullUrl is not None and fullUrl != "":
            url = fullUrl
        cache_file = self.cache_file

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
            if settings.DEBUG:
                raise e
            raise Exception("返回不是 json 内容")
        simple_cache.save_key(cache_file, uniqueStr, result, cache * 60)
        return result
    
    def get(self, api, params,**kwargs):
        return self.request(api, params, method='GET',**kwargs)
    
    def post(self, api, params,**kwargs):
        return self.request(api, params, method='POST',**kwargs)
    
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
