from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import User# , CustomUserManager
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework. permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


# These views are endpoints for the API
# to-do: add proper permissions for each endpoint. Use obj.role to determine permissions


@api_view(['GET'])
def getData(request):
    return Response({"message": "Hello, World!"})


class UserPostPermission(BasePermission):
    message = 'You are not allowed to create users.'

    def has_object_permission(self, request, view, obj):

        # need to handle anonymous users. 
        
        if request.method in SAFE_METHODS:
            return True

        
        
        return request.user.role == 'Admin'


class UserList(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    # queryset = User.objects.all()

    # Define custom queryset
    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

# class UserList(viewsets.ViewSet):
#     permission_classes = [IsAdminUser]
#     queryset = User.objects.all()

#     def list(self, request):
#         serializer_class = UserSerializer(self.queryset, many=True)
#         return Response(serializer_class.data)

#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset, pk=pk)
#         serializer_class = UserSerializer(post)
#         return Response(serializer_class.data)

    # def create(self, request):
    # def list(self, request):
    # def retrieve(self, request, pk=None):
    # def update(self, request, pk=None):
    # def partial_update(self, request, pk=None):
    # def destroy(self, request, pk=None):


# class UserList(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# # could use RetrieveUpdateDestroy instead?
# # by using the type, we can control what the api does
# class UserDetail(generics.RetrieveUpdateAPIView, UserPostPermission):
#     permission_classes = [UserPostPermission]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer