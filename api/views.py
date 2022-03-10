from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import User, CustomUserManager
from .serializers import UserSerializer


@api_view(['GET'])
def getData(request):
    return Response({"message": "Hello, World!"})


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# could use RetrieveUpdateDestroy instead?
class UserDetail(generics.RetrieveDestroyAPIView):
    pass
    # queryset = User.objects.all()
    # serializer_class = UserSerializer


