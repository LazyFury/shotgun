


from django.http import HttpRequest
from core.models import UserToken
from revolver_api.revolver_api.api import Rule, validator
from revolver_api.revolver_api.response import ApiErrorCode, ApiJsonResponse
from core.urls import api
import json

def find_device_in_ua_use_regx(ua=""):
    import re

    if re.search("iPhone", ua):
        return "iPhone"
    if re.search("Android", ua):
        return "Android"
    if re.search("Windows Phone", ua):
        return "Windows Phone"
    if re.search("Macintosh", ua):
        return "Macintosh"
    return "PC"


@api.post("login")
@validator(
    [
        Rule("username", required=True, message="用户名不能为空"),
        Rule("password", required=True, message="密码不能为空"),
    ],
    method="post",
)
def login(request: HttpRequest):
    """login


    Args:
        request (HttpRequest): _description_

    Returns:
        _type_: _description_
    """
    try:
        payload = request.valid_data or json.loads(request.body)
    except Exception as e:
        return ApiJsonResponse.error(ApiErrorCode.ERROR, e.__str__())
    # print("payload", payload)
    username = payload.get("username")
    password = payload.get("password")
    try:
        ip = request.META.get("REMOTE_ADDR")
        # print("ip", ip)
        ua = request.META.get("HTTP_USER_AGENT") or ""
        # print("ua", ua)
        is_mobile = ua.find("Mobile") > -1
        # print("is_mobile", is_mobile)
        device = find_device_in_ua_use_regx(ua)
        # print("device", device)
        token = UserToken.get_token(
            username, password, ip=ip, ua=ua, is_mobile=is_mobile, device=device
        )
    except Exception as e:
        return ApiJsonResponse.error(ApiErrorCode.USER_PASSWORD_NOT_MATCH, e.__str__())
    return ApiJsonResponse(
        {
            "token": token.token,
            "expired_at": token.expired_at,
            "user": token.user.to_json(),
        }
    )


@api.post("logout")
def logout(request: HttpRequest):
    UserToken.delete_token(request.user)
    return ApiJsonResponse.success({})


@api.get("profile")
def profile(request: HttpRequest):
    return ApiJsonResponse({"user": request.user.to_json()})