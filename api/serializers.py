from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'desk_id', 
                  'gender', 'birth_date', 'nationality', 'remote_percentage')