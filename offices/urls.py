from django.contrib import admin
from api.views import getData
from django.urls import path

urlpatterns = [
    path('' , getData),
]
