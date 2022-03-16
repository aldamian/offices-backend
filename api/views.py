from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import User, Building, Office, Desk, Request
from .serializers import UserPostSerializer, UserUpdateSerializer, RequestSerializer, BuildingSerializer, OfficeSerializer, DeskSerializer, MyTokenObtainPairSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework. permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.forms.models import model_to_dict


# These views are endpoints for the API
# to-do: add proper permissions for each endpoint. Use obj.role to determine permissions


class getRoutesView(APIView):
    permission_classes = [AllowAny]

    routes = [
        {'GET': '/swagger', 'description': 'API Documentation'},
        {'GET': '/admin', 'description': 'Admin Dashboard'},
        {'GET': '/api/users'},
        {'GET': '/api/users/<int:pk>'},
        {'GET': '/api/users/<int:pk>/requests'},
        {'GET': '/api/buildings'},
        {'GET': '/api/buildings/<int:pk>'},
        {'GET': '/api/offices'},
        {'GET': '/api/offices/<int:pk>'},
        {'GET': '/api/offices/<int:pk>/requests'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>/approve'},
        {'GET': '/api/offices/<int:pk>/requests/<int:pk>/deny'},
        {'GET': '/api/desks'},
        {'GET': '/api/desks/<int:pk>'},

        {'POST': '/api/token'},
        {'POST': '/api/token/refresh'},
        {'POST': '/api/token/blacklist'},
        {'POST': '/api/me'},
    ]

    def get(self, request):
        if request.method == 'GET':
            return Response(self.routes)


# Custom permissions for the API
class UserAuthenticatedPermission(BasePermission):
    message = 'You are not authenticated.'

    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            return True
        return False


class UserAdminPermission(BasePermission):
    message = 'You do not have Admin privileges.'

    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            user , token = response
            role = token.get('role')
            if role == 'Admin':
                return True
        return False


class UserOfficeAdminPermission(BasePermission):
    message = 'You do not have Office Admin privileges.'

    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            user , token = response
            role = token.get('role')
            if role == 'Office Admin':
                return True
        return False
            

# Display Users
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


class Me(viewsets.ViewSet):
    permission_classes = [UserAdminPermission]

    def list(self, request):
        response = JWTAuthentication().authenticate(request)
        user , token = response
        user = get_object_or_404(User, pk=user.id)
        response_fields = ['id', 'email', 'first_name', 'last_name', 'role' ]
        return JsonResponse(model_to_dict(user, fields=response_fields), safe=False)
        # return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserDetail(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [AllowAny]
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


# Display Buildings
class BuildingList(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [AllowAny]
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    def list(self, request):
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)
        return Response(serializer.data)

    # create a new building
    def create(self, request):
        serializer = BuildingSerializer(data=request.data)
        # perform validation checks
        if serializer.is_valid():
            building = Building.objects.create(
                name=serializer.validated_data['name'],
                address=serializer.validated_data['address'],
                floors_count=serializer.validated_data['floors_count'],
                img_url=serializer.validated_data['img_url'],
            )
            building.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a building
    def update(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        serializer = BuildingSerializer(building, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a building 
    # to-do: can delete only if offices are empty
    def destroy(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        building.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Display Offices
class OfficeList(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [AllowAny]
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer

    def list(self, request):
        offices = Office.objects.all()
        serializer = OfficeSerializer(offices, many=True)
        return Response(serializer.data)

    # create a new office
    def create(self, request):
        serializer = OfficeSerializer(data=request.data)
        # perform validation checks
        if serializer.is_valid():
            office = Office.objects.create(
                name=serializer.validated_data['name'],
                building_id=serializer.validated_data['building_id'],
                floor_number=serializer.validated_data['floor_number'],
                total_desks=serializer.validated_data['total_desks'],
                usable_desks=serializer.validated_data['usable_desks'],
                x_size_m=serializer.validated_data['x_size_m'],
                y_size_m=serializer.validated_data['y_size_m'],
                desk_ids=serializer.validated_data['desk_ids'],
                office_admin=serializer.validated_data['office_admin'],
            )
            office.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a office
    def update(self, request, pk=None):
        office = get_object_or_404(Office, pk=pk)
        serializer = OfficeSerializer(office, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete an office 
    # to-do: can delete only if desks are empty
    def destroy(self, request, pk=None):
        office = get_object_or_404(Office, pk=pk)
        office.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Display Desks
class DeskList(viewsets.ViewSet):
    # prod - change permission_classes to [UserAdminPermission]
    permission_classes = [AllowAny]
    queryset = Desk.objects.all()
    serializer_class = DeskSerializer

    def list(self, request):
        desks = Desk.objects.all()
        serializer = DeskSerializer(desks, many=True)
        return Response(serializer.data)

    # create a new desk
    def create(self, request):
        serializer = DeskSerializer(data=request.data)
        # perform validation checks
        if serializer.is_valid():
            desk = Desk.objects.create(
                office_id=serializer.validated_data['office_id'],
                desk_number=serializer.validated_data['desk_number'],
                user_id=serializer.validated_data['user_id'],
                is_usable=serializer.validated_data['is_usable'],
                x_size_m=serializer.validated_data['x_size_m'],
                y_size_m=serializer.validated_data['y_size_m'],
                x_pos_px=serializer.validated_data['x_pos_px'],
                y_pos_px=serializer.validated_data['y_pos_px'],
            )
            desk.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a desk
    def update(self, request, pk=None):
        desk = get_object_or_404(Desk, pk=pk)
        serializer = DeskSerializer(desk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a desk 
    # to-do: can delete only if no user is assigned
    def destroy(self, request, pk=None):
        desk = get_object_or_404(Desk, pk=pk)
        desk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    # def create(self, request):
    # def list(self, request):
    # def retrieve(self, request, pk=None):
    # def update(self, request, pk=None):
    # def partial_update(self, request, pk=None):
    # def destroy(self, request, pk=None):


# Display Requests
class RequestList(viewsets.ViewSet):
    # prod - change permission_classes to [IsAuthenticated]
    permission_classes = [AllowAny]
    serializer_class = RequestSerializer

    def list(self, request):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            user, token = response
            role = token.get('role')
            if role == 'Admin':
                # get remote pending requests
                requests = Request.objects.filter(status='P', remote_percentage__gt=0)
                return Response(RequestSerializer(requests, many=True).data)
            elif role == 'Office Admin':
                # get desk requests
                # requests = Request.objects.filter(status='P', )
                pass
                

            

    # create a new request
    def create(self, request):
        serializer = RequestSerializer(data=request.data)
        # perform validation checks
        if serializer.is_valid():
            request = Request.objects.create(
                office_id=serializer.validated_data['office_id'],
                user_id=serializer.validated_data['user_id'],
                is_approved=serializer.validated_data['is_approved'],
                is_rejected=serializer.validated_data['is_rejected'],
                is_cancelled=serializer.validated_data['is_cancelled'],
            )
            request.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class BlacklistTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

