from django.http import HttpRequest
from core import models
from core.api import Rule, Api
from .models import Link, VisitorIP
from typing import Any
from core.models import UserModel


class VisitorIPApi(Api):
    model: Any = VisitorIP

    rules = [
        Rule(name="ip", required=True, message="ip不能为空"),
    ]


class LinkApi(Api):
    model: Any = Link

    rules = [
        Rule(name="url", required=True, message="url不能为空"),
    ]

    @property
    def urls(self):
        return self.get_urls() + [], "link", "link"
    
    def defaultQuery(self, **kwargs):
        return super().defaultQuery(**kwargs) #.order_by("-posted_by__is_active")


def noAuth(func: Any):
    def wrapper(self, request, *args, **kwargs):
        print("noAuth wrapper")
        return func(self, request, *args, **kwargs)

    return wrapper


class UserApi(Api):
    model: Any = UserModel

    rules = []

    @noAuth
    def pageApi(self, request: HttpRequest, **kwargs):
        return super().pageApi(request, **kwargs)


linkApi = LinkApi()
visitorIp = VisitorIPApi()
userApi = UserApi()



