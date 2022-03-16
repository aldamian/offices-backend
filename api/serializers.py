from rest_framework import serializers
from .models import User, Building, Office, Desk, Request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'first_name', 'last_name', 'office_id', 'building_id', 
                  'gender', 'birth_date', 'nationality', 'remote_percentage')
    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('email', 'password', 'role', 'first_name', 'last_name', 'office_id', 'building_id',
                  'gender', 'birth_date', 'nationality', 'remote_percentage', 'img_url', 'is_active')


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('user_id', 'office_id', 'remote_percentage', 'request_reason', 'status', 'reject_reason')


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('name', 'address', 'floors_count', 'img_url')


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('name', 'building_id', 'floor_number', 'total_desks', 'usable_desks', 
                  'x_size_m', 'y_size_m', 'desk_ids', 'office_admin')


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ('office_id', 'desk_number', 'user_id', 'is_usable',
                  'x_size_m', 'y_size_m', 'x_pos_px', 'y_pos_px')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claims
        token['user_id'] = user.id
        token['role'] = user.role
        
        return token