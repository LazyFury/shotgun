

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