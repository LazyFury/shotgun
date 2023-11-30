from django.urls import path

from libs.utils import func1

from .views import jump, qecodeGenerate, home
from .api import urls as api_urls

urlpatterns = [
    path("j/<str:path>", jump, name="jump"),
    path("qr", qecodeGenerate, name="qrcode"),
    path("", home),
] + api_urls

func1()