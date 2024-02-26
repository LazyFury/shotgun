from hashlib import md5
import json
import random
import time
import requests
import simple_cache
from backend import settings
from core import config

# disable requests  SSL warning
requests.packages.urllib3.disable_warnings()

class DtkClient():
    def __init__(self):
        self.baseUrl = config.get("dtk.apiUrl")
        self.version = config.get("dtk.version")
        self.appKey =  config.get("dtk.appKey")
        self.appSerect = config.get("dtk.appSecret")
        self.cache_file = config.get_cache_file("dtk.cache")
        if not self.baseUrl:
            raise Exception("dtk.apiUrl is required")
        if not self.version:
            raise Exception("dtk.version is required")
        if not self.appKey:
            raise Exception("dtk.appKey is required")
        if not self.appSerect:
            raise Exception("dtk.appSecret is required")
    
    
    def request(self, api, params,method='GET',fullUrl="",cache=5,**kwargs):
        url = self.baseUrl + api
        print("dtk request url:",url)
        if fullUrl is not None and fullUrl != "":
            url = fullUrl
        cache_file = self.cache_file
        # print("request",url, params)
        uniqueStr = md5((method + url + json.dumps(params)).encode('utf-8')).hexdigest()
        cached =  simple_cache.load_key( cache_file,uniqueStr)
        if cached is not None:
            # print("load from cache", cache_file, uniqueStr)
            return cached
        params =  self.sign(params)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
            'Client-Sdk-Type':'python',
            'Content-Type':'application/json'
        }
        
        try:
            resp =  requests.request(method, url, params=params,headers=headers,verify=False,**kwargs)
            if resp.status_code != 200:
                raise Exception(f"请求失败,状态码：{resp.status_code}")
            result = resp.json()
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
        nonce = random.randint(100000, 999999)
        timer = int(time.time() * 1000)
        # print("timerr",timer)
        appKey = self.appKey
        key = self.appSerect
        str = f'appKey={appKey}&timer={timer}&nonce={nonce}&key={key}'
        # print("str",str)
        params['signRan'] =  md5(str.encode('utf-8')).hexdigest().upper()
        params['timer'] = timer
        params['nonce'] = nonce
        params['version'] = self.version
        params['appKey'] = self.appKey
        params['appSecret'] = self.appSerect
        return params
