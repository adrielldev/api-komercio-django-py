from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        read_only_fields = ['is_active']
        exclude = ['last_login','groups','user_permissions','email','is_staff']
        
        
    def create(self,validated_data:dict): 

        return User.objects.create_user(**validated_data)


