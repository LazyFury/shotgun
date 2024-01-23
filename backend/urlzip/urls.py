from importlib import import_module
from django.urls import path
from .views import genMpMiniQrcode, getRandomString, jump, qecodeGenerate, home, sendMpMiniSubscribe

import_module("urlzip.api")

urlpatterns = [
    path("j/<str:path>", jump, name="jump"),
    path("qr", qecodeGenerate, name="qrcode"),
    path("", home),
    path('wxmini/send',sendMpMiniSubscribe),
    path('wxmini/qr',genMpMiniQrcode),
    path('api/random',getRandomString)
]
