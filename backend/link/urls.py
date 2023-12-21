from django.urls import path

from libs.utils import func1

from .views import genMpMiniQrcode, jump, qecodeGenerate, home, sendMpMiniSubscribe
from .api import urls as api_urls

urlpatterns = [
    path("j/<str:path>", jump, name="jump"),
    path("qr", qecodeGenerate, name="qrcode"),
    path("", home),
    path('wxmini/send',sendMpMiniSubscribe),
    path('wxmini/qr',genMpMiniQrcode),
] + api_urls

func1()