
import datetime
import requests
from core import config


class WxException(Exception):
    raw = ''
    msg = ''
    
    def __init__(self,msg, raw=None):
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
        """获取 access_token

        Raises:
            WxException: _description_
            WxException: _description_

        Returns:
            _type_: _description_
        """
        if 'access_token' in self.memcache and 'expire' in self.memcache and self.memcache['expire'] > datetime.datetime.now().timestamp():
            print('get access_token from memcache')
            return self.memcache['access_token'], self.memcache['expire']
        if self.appkey is None or self.appSerect is None:
            raise WxException("appkey 或 appSerect 未设置")
        
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
        """发布订阅消息

        Args:
            openid (_type_): _description_
            template_id (_type_): _description_
            page (_type_): _description_
            data (_type_): _description_

        Raises:
            WxException: _description_

        Returns:
            _type_: _description_
        """
        access_token, expire = self.getAccessToken()
        if access_token is None:
            raise WxException("获取 access_token 失败")
        if expire < datetime.datetime.now().timestamp():
            raise WxException("access_token 过期")
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
    
mpminiClient = MpMiniClient(config.get('minimp.appid'),config.get("minimp.screct"))