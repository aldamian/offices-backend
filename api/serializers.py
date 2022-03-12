from rest_framework import serializers
from .models import User, Building, Office, Desk, Desk_Request, Remote_Request
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'first_name', 'last_name', 'desk_id', 
                  'gender', 'birth_date', 'nationality', 'remote_percentage')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role
        token['email'] = user.email
        token['password'] = user.password
        # ...

        return token