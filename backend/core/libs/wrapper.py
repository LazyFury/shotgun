


from re import A
from django.http import HttpRequest
from core.models import UserPermission
from revolver_api.revolver_api.response import ApiErrorCode, ApiJsonResponse
from revolver_api.revolver_api.utils.get_request_args import get_instance_from_args_or_kwargs
from django.contrib.auth.models import AnonymousUser

def hasPermission(permission="",allow_superuser=True):
    """ 检查权限

    Args:
        permission (str, optional): _description_. Defaults to "".
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            request = get_instance_from_args_or_kwargs(HttpRequest, args, kwargs)
            user = request.user
            if isinstance(user,AnonymousUser):
                return ApiJsonResponse.error(ApiErrorCode.ERROR, "用户未登录")
            if permission in ["","#", None]:
                print("dont need permission check")
                return func(*args, **kwargs)
            if user.is_superuser and allow_superuser:
                return func(*args, **kwargs)
            user_permissions = UserPermission.objects.filter(user=user)
            for user_permission in user_permissions:
                if user_permission.permission.code == permission:
                    return func(*args, **kwargs)
            return ApiJsonResponse.error(ApiErrorCode.ERROR, "没有权限")
        return inner
    return wrapper
        