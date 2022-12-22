from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id','password','is_superuser','username',
            'email','is_active','phone'
        ]
        extra_kwargs = {
            'username': {'max_length': 16, 'min_length':6},
            'password': {"write_only": True},
            'is_superuser': {'default': False},
            'is_active': {'default': False}
        }
    def validate_password(self,value):
        if 4 <= len(value) <= 16:
            return make_password(value)
        raise serializers.ValidationError("密码的长度需要4到16个字符")
