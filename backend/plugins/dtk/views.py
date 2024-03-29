from django.shortcuts import render
from core.libs.wrapper import hasPermission
from revolver_api.revolver_api.api import ApiErrorCode, ApiJsonResponse, Rule, validator

from . import DtkClient

client = None

def get_client():
    global client
    if not client:
        try:
            client = DtkClient.DtkClient()
        except Exception as e:
            print("get_client error", e)
    return client

# Create your views here.
@hasPermission("dtk",allow_superuser=True)
@validator([
    Rule("url", required=True, type=str,message="url is required"),
])
def dataoke(request):
    """获取大淘客数据api 说明：https://www.dataoke.com/

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("dataoke request",request.GET.dict())
    client = get_client()
    params = request.GET.dict()
    url = params.get("url", "")
    cache = params.get("cache", 5)
    # print("dataoke url",url)
    result = client.get(url, {
        **params,
    },cache=int(cache))
    # print("dataoke result",result)
    return ApiJsonResponse.success(
        result,
        message=result["msg"] if "msg" in result else "success",
    )