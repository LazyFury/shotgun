


from django.http import HttpRequest
from core.response import ApiJsonResponse
from core.route import Router


@Router.get("api/test",exception_json=True)
def test(request: HttpRequest):
    raise Exception("test error")
    def randomStr(length=10):
        import random
        import string
        return ''.join(random.sample(string.ascii_letters + string.digits, length))
    return ApiJsonResponse({
        str(k) +"message" :randomStr() for k in range(10)
    })
    
    

@Router.get("api")
def api(request: HttpRequest):
    return ApiJsonResponse({
        "name": "api",
        "connect": "success",
    })
    
@Router.get("test")
def test(request):
    return ApiJsonResponse.success({
        'method': request.method,
    })