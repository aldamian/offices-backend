from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import User# , CustomUserManager
from .serializers import UserUpdateSerializer, UserPostSerializer, UserUpdateSerializer, MyTokenObtainPairSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework. permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.forms.models import model_to_dict
# import JsonResponse
# 

# These views are endpoints for the API
# to-do: add proper permissions for each endpoint. Use obj.role to determine permissions


class getRoutesView(APIView):
    permission_classes = [AllowAny]

    routes = [
        {'GET': '/swagger/', 'description': 'API Documentation'},
        {'GET': '/admin/', 'description': 'Admin Dashboard'},
        {'GET': '/api/users/'},
        {'GET': '/api/users/<int:pk>/'},
        {'GET': '/api/users/<int:pk>/requests/'},
        {'GET': '/api/buildings/'},
        {'GET': '/api/buildings/<int:pk>/'},
        {'GET': '/api/offices/'},
        {'GET': '/api/offices/<int:pk>/'},
        {'GET': '/api/offices/<int:pk>/requests/'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>/'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>/approve/'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>/deny/'},
        {'GET': '/api/desks/'},
        {'GET': '/api/desks/<int:pk>/'},

        {'POST': '/api/token/'},
        {'POST': '/api/token/refresh'},
        {'POST': '/login/'},
    ]

    def get(self, request):
        if request.method == 'GET':
            return Response(self.routes)



class UserAdminPermission(BasePermission):
    message = 'You are not allowed to create users.'

    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            user , token = response
            role = token.get('role')
            if role == 'Admin':
                return True
            return False
            

# Display Users


class UserList(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]

    def get_query_set(self):
        return User.objects.all()

    def get_serializer_class(self, *args, **kwargs):
            return UserPostSerializer

    def list(self, request):
        queryset = self.get_query_set()
        serializer = self.get_serializer_class()
        result = serializer(queryset, many=True)
        return Response(result.data)

    # def create(self, request):
    #     serializer = self.get_serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def retrieve(self, request, pk=None):
    #     queryset = self.get_query_set()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = self.get_serializer_class(user)
    #     return Response(serializer.data)

    # def partial_update(self, request, pk=None):
    #     queryset = self.get_query_set()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = self.get_serializer_class(user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


class patchUser(viewsets.ViewSet):
    serializer_class = UserUpdateSerializer
    permission_classes = [UserAdminPermission]


    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class postUser(viewsets.ViewSet):
    serializer_class = UserPostSerializer
    permission_classes = [UserAdminPermission]

    def create(self, request):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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