from django.urls import path
from .views import BlacklistTokenView, UserList, UserDetail


app_name = 'api'

urlpatterns = [
    path('<int:pk>/', UserDetail.as_view(), name='detailcreate'),
    path('', UserList.as_view(), name='listcreate'),
    path('logout/blacklist/', BlacklistTokenView.as_view(), name='blacklist_token')
]