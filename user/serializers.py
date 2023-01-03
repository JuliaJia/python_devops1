from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
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
            'username': {'max_length': 16, 'min_length':4},
            'password': {"write_only": True},
            'is_superuser': {'default': False},
            'is_active': {'default': False}
        }
    def validate_password(self,value):
        if 8 <= len(value) <= 16:
            return make_password(value)
        raise serializers.ValidationError("密码的长度需要8到16个字符")



class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class PermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
    content_type = ContentTypeSerializer(read_only=True)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'