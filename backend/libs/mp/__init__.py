
import datetime
from email import message
import json
import requests

from config import minimp


class WxException(Exception):
    raw = ''
    msg = ''
    
    def __init__(self,msg, raw):
        self.msg = msg
        self.raw = raw
        
    def __str__(self):
        return self.msg
    
    @property
    def data(self):
        return {
            "raw": self.raw,
        }
    

class MpMiniClient:
    appkey = 'appkey'
    appSerect = 'appSerect'
    
    def __init__(self, appkey, appSerect):
        self.appkey = appkey
        self.appSerect = appSerect
    
    memcache = {}
        
    def getAccessToken(self):
        if 'access_token' in self.memcache and 'expire' in self.memcache and self.memcache['expire'] > datetime.datetime.now().timestamp():
            print('get access_token from memcache')
            return self.memcache['access_token'], self.memcache['expire']
        
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + self.appkey + '&secret=' + self.appSerect
        res = requests.get(url)
        result = res.json()
        if 'errcode' in result:
            raise WxException("获取 access_token 失败",result)
        expire = result['expires_in']
        access_token = result['access_token']
        self.memcache['access_token'] = access_token
        self.memcache['expire'] = datetime.datetime.now().timestamp() + expire
        return access_token, expire
    
    def sendSubscribeMessage(self, openid, template_id, page, data):
        access_token, expire = self.getAccessToken()
        url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + access_token
        data = {
            'touser': openid,
            'template_id': template_id,
            'page': page,
            'data': data
        }
        res = requests.post(url, json=data)
        result = res.json()
        if 'errcode' in result:
            return result
        return result
    
    def getUnlimited(self, page='pages/index/index', scene="1", width=430, auto_color=False, line_color=None, is_hyaline=False):
        access_token, expire = self.getAccessToken()
        url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + access_token
        data = {
            'scene': scene,
            'page': page,
            'width': width,
            'auto_color': auto_color,
            'line_color': line_color,
            'is_hyaline': is_hyaline
        }
        res = requests.post(url, json=data)
        # if stream 
        if res.headers['Content-Type'] == 'image/jpeg':
            return res.content
        return res.json()
    
mpminiClient = MpMiniClient(minimp.APPID,minimp.SECRET)