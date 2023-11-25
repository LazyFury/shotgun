from typing import Any
from django.urls import path
from .views import jump, qecodeGenerate, home
from .models import VisitorIPApi, Link
from core.api import Api

visitorIp = VisitorIPApi()


class LinkApi(Api):
    model: Any = Link


linkApi = LinkApi()

apis = [
    path("api/visitor_ip/", visitorIp.urls),  # type: ignore
    path("api/link/", linkApi.urls, name="link"),
]


urlpatterns = [
    path("j/<str:path>", jump, name="jump"),
    path("qr", qecodeGenerate, name="qrcode"),
    path("", home),
] + apis
