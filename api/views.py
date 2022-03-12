from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import User# , CustomUserManager
from .serializers import UserSerializer
from rest_framework. permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions


# These views are endpoints for the API
# Remove graphical views from API


@api_view(['GET'])
def getData(request):
    return Response({"message": "Hello, World!"})


class UserPostPermission(BasePermission):
    message = 'You are not allowed to create users.'

    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True
        
        return obj.role == 'Admin' 


class UserList(generics.ListCreateAPIView):
    # permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


# could use RetrieveUpdateDestroy instead?
# by using the type, we can control what the api does
class UserDetail(generics.RetrieveUpdateAPIView, UserPostPermission):
    permission_classes = [UserPostPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer


