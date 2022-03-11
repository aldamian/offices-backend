from django.contrib import admin
from api.views import getData
from django.urls import path, include


urlpatterns = [
    path('' , getData),
    path('api/', include('api.urls', namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
