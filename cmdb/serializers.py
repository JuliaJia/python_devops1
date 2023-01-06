from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework_mongoengine import fields
from .models import CiType,Ci

class CiTypeSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = CiType
        fields = '__all__'
        # exclude = ['fields']


class CiTypeWithFieldsSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = CiType
        fields = '__all__'
        # exclude = ['fields']

class CiSerializer(mongoserializers.DynamicDocumentSerializer):
    # id = fields.ObjectIdField()
    class Meta:
        model = Ci
        fields = '__all__'


class CiWithIdSerializer(mongoserializers.DynamicDocumentSerializer):
    id = fields.ObjectIdField()
    class Meta:
        model = Ci
        fields = '__all__'