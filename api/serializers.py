from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'role', 'first_name', 'last_name', 'desk_id', 
                  'gender', 'birth_date', 'nationality', 'remote_percentage')