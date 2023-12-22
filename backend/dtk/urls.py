

from django.urls import path

from dtk.views import dataoke


urlpatterns = [
    path('',dataoke)
]