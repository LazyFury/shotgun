from multiprocessing.managers import BaseManager
from django.http import HttpRequest
from core.api import Rule, Api
from .models import Link, VisitorIP
from typing import Any
from core.models import UserModel


class VisitorIPApi(Api):
    model = VisitorIP

    rules = [
        Rule(name="ip", required=True, message="ip不能为空"),
    ]


class LinkApi(Api):
    model = Link

    rules = [
        Rule(name="url", required=True, message="url不能为空"),
    ]

    @property
    def urls(self):
        return self.get_urls() + [], "link", "link"
    
    def defaultQuery(self, **kwargs):
        return super().defaultQuery(**kwargs) #.order_by("-posted_by__is_active")


class UserApi(Api):
    model = UserModel

    rules = []

    def pageApi(self, request: HttpRequest, **kwargs):
        return super().pageApi(request, **kwargs)


linkApi = LinkApi()
visitorIp = VisitorIPApi()
userApi = UserApi()



