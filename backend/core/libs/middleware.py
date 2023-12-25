

from core import config
from core.api import ApiErrorCode, ApiJsonResponse


def APITokenAuthMiddleware(get_response):
    """Middleware to authenticate API requests using token authentication."""
    def inner(request):
            if request.path.startswith('/___api/'):
                try:
                    token = request.headers.get("token")
                    print("token", token)
                    if token == "123456":
                        return get_response(request)
                    return ApiJsonResponse.error(ApiErrorCode.TOKEN_INVALID, "Token invalid")
                except Exception as e:
                    return ApiJsonResponse.error(ApiErrorCode.ERROR, e.__str__())
            return get_response(request)
    return inner

def RatelimitMiddleware(get_response):
    import simple_cache
    cache_file = config.cacheFile("rate.cache")
    """Middleware to authenticate API requests using token authentication."""
    def inner(request):
            if request.path.startswith('/api/'):
                count = simple_cache.load_key(cache_file,'count') or 0
                print("count", count)
                if count > 60:
                    return ApiJsonResponse.error(ApiErrorCode.ERROR, "每秒请求数超过50次")
                simple_cache.save_key(cache_file,'count', count+1, 1)
            return get_response(request)
    return inner