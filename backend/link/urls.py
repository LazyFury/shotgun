from email import message
from typing import Any
from django.http import HttpRequest
from django.urls import path
from .views import jump, qecodeGenerate, home
from .models import Link, VisitorIP
from core.api import Api, Rule


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


linkApi = LinkApi()
visitorIp = VisitorIPApi()


apis = [
    path("api/ip/", visitorIp.urls),  # type: ignore
    path("api/link/", linkApi.urls),  # type: ignore
]


urlpatterns = [
    path("j/<str:path>", jump, name="jump"),
    path("qr", qecodeGenerate, name="qrcode"),
    path("", home),
] + apis
