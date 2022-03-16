from .models import User
from .serializers import UserPostSerializer, UserUpdateSerializer
from .permissions import UserAuthenticatedPermission, UserAdminPermission, UserOfficeAdminPermission
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.forms.models import model_to_dict


# Display Users
class Me(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]

    def list(self, request):
        response = JWTAuthentication().authenticate(request)
        user , token = response
        user = get_object_or_404(User, pk=user.id)
        response_fields = ['id', 'email', 'first_name', 'last_name', 'role' ]
        return JsonResponse(model_to_dict(user, fields=response_fields), safe=False)

        
class UserList(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]
    queryset = User.objects.all()
    serializer_class = UserPostSerializer

    def list(self, request):
        users = User.objects.all()
        serializer = UserPostSerializer(users, many=True)
        return Response(serializer.data)

    # create a new user with CustomUserManager
    def create(self, request):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_superuser(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                role=serializer.validated_data['role'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                office_id=serializer.validated_data['office_id'],
                building_id=serializer.validated_data['building_id'],
                gender=serializer.validated_data['gender'],
                birth_date=serializer.validated_data['birth_date'],
                nationality=serializer.validated_data['nationality'],
                remote_percentage=serializer.validated_data['remote_percentage'],
            )
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]
    serializer_class = UserUpdateSerializer

    # Display a single user
    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)

    # Update a user
    # to-do: handle password update
    def update(self, request, pk=None):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            user , token = response
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                user.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

