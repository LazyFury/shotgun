from django.urls import path
from .views import jump, qecodeGenerate, home, getShortUrl
from .models import VisitorIPApi

visitorIp = VisitorIPApi()

apis = [
    path("api/short/<int:pk>", getShortUrl, name="getShortUrl"),
    path("api/visitorip/", visitorIp.urls),  # type: ignore
]


urlpatterns = [
    path("j/<str:path>", jump, name="jump"),
    path("qr", qecodeGenerate, name="qrcode"),
    path("", home),
] + apis
