from django.shortcuts import render
from core.api import ApiErrorCode, ApiJsonResponse

from core.libs import DtkClient

client = DtkClient.DtkClient()
# Create your views here.
def dataoke(request):
    params = request.GET.dict()
    url = params.get("url", "")
    if url == "":
        return ApiJsonResponse.error(ApiErrorCode.ERROR, "url is empty")
    result = client.get(url, {
        **params,
    })
    
    return ApiJsonResponse.success(result) 