# from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from rest_framework_mongoengine import viewsets
from rest_framework.decorators import action
from .models import CiType,Ci
from .serializers import CiTypeSerializer, CiSerializer, CiTypeWithFieldsSerializer,CiWithIdSerializer
from mongoengine.queryset.visitor import Q
# from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes,action
import sys
# Create your views here.
sys.path.append("..")
from utils.permissions import IsCMDBer
# from user.models import UserProfile
from rest_framework import filters
from rest_framework.fields import SkipField


class CiTypeViewSet(viewsets.ModelViewSet):
    queryset = CiType.objects.all()
    serializer_class = CiTypeWithFieldsSerializer
    permission_classes = [IsCMDBer]
    filter_backends = [filters.SearchFilter]
    search_fields = ['label', 'name']
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request,*args, **kwargs)
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        label = self.request.query_params.get('label', None)
        if name or label:
            queryset = queryset.filter(Q(name__icontains=name) | Q(label__icontains=label))
        return queryset
    @action(detail=False)
    def all(self,request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset,many=True)
        data = serializer.data
        return Response(data)

    def get_serializer_class(self):
        if 'id' not in self.kwargs:
            return CiTypeSerializer
        return super().get_serializer_class()

    @action(detail=False,url_path="(?P<name>[^/.]+)/(?P<version>\d+)")
    def get_by_name_and_version(self,request,name,version):
        obj = self.get_queryset().get(name=name,version=version)
        serializer = CiTypeWithFieldsSerializer(obj)
        return Response(serializer.data)


class CiViewSet(viewsets.ModelViewSet):
    queryset = Ci.objects.all()
    serializer_class = CiSerializer
    permission_classes = [IsCMDBer]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['label', 'name']
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request,*args, **kwargs)
    def get_queryset(self):
        queryset = super().get_queryset()
        value = self.request.query_params.get('value', None)
        if value:
            queryset = queryset.filter(Q(fields__value__icontains=value))
        return queryset

class CiWithIdViewSet(viewsets.ModelViewSet):
    queryset = Ci.objects.all()
    serializer_class = CiWithIdSerializer
    permission_classes = [IsCMDBer]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['label', 'name']
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request,*args, **kwargs)

