# from django.urls import path
from .views import BlacklistTokenView, UserList, patchUser
from rest_framework.routers import DefaultRouter


app_name = 'api'

# urlpatterns = [
#     path('<int:pk>/', UserDetail.as_view(), name='detailcreate'),
#     path('', UserList.as_view(), name='listcreate'),
#     path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist_token')
# ]

router = DefaultRouter()
router.register('users', UserList, basename='post')

urlpatterns = router.urls