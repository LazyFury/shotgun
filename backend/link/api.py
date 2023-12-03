from django.http import HttpRequest
from core.api import Rule, Api
from .models import Link, VisitorIP
from typing import Any
from django.urls import path

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


urls = [
    path("api/ip/", visitorIp.urls),  # type: ignore
    path("api/link/", linkApi.urls),  # type: ignore
    path("api/user/", userApi.urls),  # type: ignore
]
