from rest_framework_mongoengine import serializers as mongoserializers
from .models import CiType

class CiTypeSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = CiType
        # fields = '__all__'
        exclude = ['fields']