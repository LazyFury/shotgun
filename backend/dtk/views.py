from django.shortcuts import render
from revolver_api.revolver_api.api import ApiErrorCode, ApiJsonResponse, Rule, validator

from dtk import DtkClient

client = DtkClient.DtkClient()
# Create your views here.
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
    params = request.GET.dict()
    url = params.get("url", "")
    cache = params.get("cache", 5)
    if url == "":
        return ApiJsonResponse.error(ApiErrorCode.ERROR, "url is empty")
    result = client.get(url, {
        **params,
    },cache=int(cache))
    
    return ApiJsonResponse.success(
        result,
        message=result["msg"] if "msg" in result else "success",
    )