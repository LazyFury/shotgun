from core.api import Rule, Api
from .models import Link, VisitorIP
from typing import Any
from django.urls import path


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


linkApi = LinkApi()
visitorIp = VisitorIPApi()


urls = [
    path("api/ip/", visitorIp.urls),  # type: ignore
    path("api/link/", linkApi.urls),  # type: ignore
]
