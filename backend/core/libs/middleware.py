

from core import config
from core.models import UserToken
from revolver_api.revolver_api.api import ApiErrorCode, ApiJsonResponse

def APIAuthMiddleware(prefix="/api", exclude=["/api/login"]):
    def midd(get_response):
        """Middleware to authenticate API requests using token authentication."""
        def inner(request):
                # exclude /login 
                if request.path in exclude:
                    return get_response(request)
                if request.path.startswith(prefix):
                    try:
                        token = request.headers.get("Token")
                        print("token", token)
                        checked_user = UserToken.check_token(token)
                        if checked_user is not None:
                            request.user = checked_user
                            return get_response(request)
                        return ApiJsonResponse.error(ApiErrorCode.TOKEN_INVALID, "Token invalid")
                    except Exception as e:
                        return ApiJsonResponse.error(ApiErrorCode.ERROR, e.__str__())
                return get_response(request)
        return inner
    return midd

def RatelimitMiddleware(get_response):
    import simple_cache
    cache_file = config.get_cache_file("rate.cache")
    """Middleware to authenticate API requests using token authentication."""
    def inner(request):
            if request.path.startswith('/api/'):
                count = simple_cache.load_key(cache_file,'count') or 0
                print("count", count)
                if count > 1000:
                    return ApiJsonResponse.error(ApiErrorCode.ERROR, "每秒请求数超过50次")
                simple_cache.save_key(cache_file,'count', count+1, 1)
            return get_response(request)
    return inner


def CorsAcceptMiddleware(get_response):
    """Middleware to authenticate API requests using token authentication."""
    def inner(request):
            if request.method == "OPTIONS":
                response = ApiJsonResponse.success({})
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
        
            if request.path.startswith('/'):
                response = get_response(request)
                response["Access-Control-Allow-Origin"] = "*"
                response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
                response["Access-Control-Max-Age"] = "1000"
                response["Access-Control-Allow-Headers"] = "*"
                return response
            return get_response(request)
    return inner

