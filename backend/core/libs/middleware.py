

import os
from core import config
from core.models import UserToken
from revolver_api.revolver_api.api import ApiErrorCode, ApiJsonResponse

def APIAuthMiddleware(prefix="/api", exclude=["/api/login"]):
    def midd(get_response):
        """Middleware to authenticate API requests using token authentication."""
        def inner(request):
                # exclude /login 
                
                if request.path.startswith(prefix):
                    try:
                        token = request.headers.get("Token") or ""
                        print("token", token)
                        try:
                            checked_user = UserToken.check_token(token)
                        except Exception:
                            checked_user = None
                        if checked_user is not None:
                            request.user = checked_user
                            return get_response(request)
                        # 不要求必须登录，但是如果登录了，还是要绑定用户
                        if request.path in exclude:
                            return get_response(request)

                        if token == "":
                            return ApiJsonResponse.error(ApiErrorCode.USER_NOT_LOGIN, "Token not found")
                        return ApiJsonResponse.error(ApiErrorCode.TOKEN_INVALID, "Token invalid")
                    except Exception as e:
                        return ApiJsonResponse.error(ApiErrorCode.ERROR, e.__str__())
                return get_response(request)
        return inner
    return midd


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

