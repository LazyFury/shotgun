from django.http import HttpRequest
from django.shortcuts import redirect, render
from core.response import ApiJsonResponse

from core.route import DApi, Router


# Create your views here.
def handler404(request, exception):
    return render(request, "404.html", status=404)


def logout(request):
    from django.contrib.auth import logout

    logout(request)
    return redirect("/")


@DApi.get("test",exception_json=True)
def test(request: HttpRequest):
    def randomStr(length=10):
        import random
        import string
        return ''.join(random.sample(string.ascii_letters + string.digits, length))
    return ApiJsonResponse({
        str(k) +"message" :randomStr() for k in range(10)
    })
    
    

@DApi.get("v2",description="所有接口")
def api(request: HttpRequest):
    return ApiJsonResponse({
        "name": "api",
        "connect": "success",
        "routers":Router.routes
    })