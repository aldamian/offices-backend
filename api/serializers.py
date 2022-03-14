from rest_framework import serializers
from .models import User, CustomUserManager, Building, Office, Desk, Request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'first_name', 'last_name', 'office_id', 'building_id', 
                  'gender', 'birth_date', 'nationality', 'remote_percentage')
    
    # here I need to check token and role
    def create(self, validated_data):
        pass 


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ('email', 'password', 'role', 'first_name', 'last_name', 'office_id', 'building_id',
                  'gender', 'birth_date', 'nationality', 'remote_percentage', 'img_url', 'is_active')
        
    def update(self, validated_data):
        pass


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('user_id', 'office_id', 'remote_percentage', 'request_reason', 'status', 'reject_reason')


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ('name', 'floor_count', 'address', 'img_url')


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('name', 'building_id', 'floor_number', 'total_desks', 'usable_desks', 'office_admin')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claims
        token['role'] = user.role
        token['email'] = user.email
        token['password'] = user.password

        return token