
from functools import wraps
from django.http import HttpRequest
from django.urls import path
from core.api import ApiErrorCode, ApiJsonResponse


def valid_method_middlewares(method="GET"):
    def middleware(request:HttpRequest):
        print("valid_method_middlewares",request.method,method)
        if request.method == method:
            return True
        else:
            raise Exception("不支持的请求方法")
    return middleware


class Route():
    """_summary_
    """
    
    urls = []
    routes = []
    
    def route(self,url, middlewares=[],name_suffix=""):
        """_summary_

        Args:
            url (_type_): _description_
            middlewares (list, optional): _description_. Defaults to [].
        """
        def decorator(func):

            @wraps(func)
            def inner(request: HttpRequest, *args, **kwargs):
                for middleware in middlewares:
                    try:
                        next = middleware(request)
                        if next:
                            return func(request, *args, **kwargs)
                    except Exception as e:
                        return ApiJsonResponse.error(ApiErrorCode.ERROR,str(e))
                    
            self.urls.append(path(url, inner, name=func.__name__ + name_suffix))
            return inner
            
        return decorator
    
    def get(self,url,middlewares=[]):
        return self.route(url,middlewares=[valid_method_middlewares("GET")] + middlewares,name_suffix="_get")

    def post(self,url,middlewares=[]):
        return self.route(url,middlewares=[valid_method_middlewares("POST")] + middlewares,name_suffix="_post")
    
    def put(self,url,middlewares=[]):
        return self.route(url,middlewares=[valid_method_middlewares("PUT")] + middlewares,name_suffix="_put")
    
    def delete(self,url,middlewares=[]):
        return self.route(url,middlewares=[valid_method_middlewares("DELETE")] + middlewares,name_suffix="_delete")
    
    
route = Route()

@route.get("test")
def test(request):
    return ApiJsonResponse.success({
        'method': request.method,
    })
