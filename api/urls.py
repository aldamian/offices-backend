# from django.urls import path
from .views import Me, UserList, UserDetail, BuildingList, OfficeList, DeskList 
from rest_framework.routers import DefaultRouter


app_name = 'api'


router = DefaultRouter()
router.register('me', Me, basename='me')
router.register('users', UserList, basename='post')
router.register('users', UserDetail, basename='update')
router.register('buildings', BuildingList, basename='post')
router.register('offices', OfficeList, basename='post')
router.register('desks', DeskList, basename='post')

urlpatterns = router.urls