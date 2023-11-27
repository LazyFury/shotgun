import time
import requests

from config import minimp


class MiniMpWx:
    class SessionInfo:
        openid = None
        session_key = None
        unionid = None
        errcode = None

        def __init__(self, openid, session_key, unionid, errcode):
            self.openid = openid
            self.session_key = session_key
            self.unionid = unionid
            self.errcode = errcode

    def __init__(self):
        self.appid = minimp.APPID
        self.secret = minimp.SECRET
        self.access_token = None
        self.expires_in = None
        self.expires_time = None
        self.get_access_token()
        self.session_key = None
        self.session_info = None

    def get_access_token(self):
        if (
            self.access_token is None
            or self.expires_time is None
            or self.expires_time < time.time()
        ):
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(
                self.appid, self.secret
            )
            response = requests.get(url)
            data = response.json()
            self.access_token = data["access_token"]
            self.expires_in = data["expires_in"]
            self.expires_time = time.time() + self.expires_in
        else:
            print("token not expired")
        return self.access_token

    def get_qrcode(self, scene):
        self.get_access_token()
        url = "https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token={}".format(
            self.access_token
        )
        data = {
            "scene": scene,
            "page": "pages/index/index",
            "width": 430,
            "auto_color": False,
            "line_color": {"r": 0, "g": 0, "b": 0},
            "is_hyaline": False,
        }
        response = requests.post(url, json=data)
        return response.content

    def code2session(self, js_code):
        url = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code".format(
            self.appid, self.secret, js_code
        )
        response = requests.get(url)
        try:
            self.session_key = response.json()["session_key"]
            self.session_info = self.SessionInfo(
                response.json()["openid"],
                self.session_key,
                response.json()["unionid"],
                response.json()["errcode"],
            )
        except Exception as e:
            print(e)
        return response.json()

    def decodeUserInfo(self, code, encryptedData, iv):
        from Crypto.Cipher import AES
        import base64
        import json

        if self.session_key is None:
            self.code2session(code)
        sessionKey = base64.b64decode(self.session_key)  # type: ignore
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)
        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
        result = cipher.decrypt(encryptedData)
        result = json.loads(result)
        return result

    def templateNotify(self, form_id, data, page="pages/index/index"):
        self.get_access_token()
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={}".format(
            self.access_token
        )
        if self.session_info is None or self.session_info.openid is None:
            return {"error": "openid is required"}
        data = {
            "touser": self.session_info.openid,
            "template_id": "4U3YJQq3XZa9xqZoRb8rWj5pZyZq9G4Yl6W3xP6Y0Zs",
            "page": page,
            "form_id": form_id,
            "data": data,
        }
        response = requests.post(url, json=data)
        return response.json()
