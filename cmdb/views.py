# from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from rest_framework_mongoengine import viewsets
from .models import CiType
from .serializers import CiTypeSerializer
# from rest_framework.permissions import IsAuthenticated,IsAdminUser
# from rest_framework.request import Request
# from rest_framework.decorators import api_view, permission_classes,action
import sys
# Create your views here.
sys.path.append("..")
from utils.permissions import IsCMDBer
# from user.models import UserProfile



class CiTypeViewSet(viewsets.ModelViewSet):
    queryset = CiType.objects.all()
    serializer_class = CiTypeSerializer
    permission_classes = [IsCMDBer]
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request,*args, **kwargs)





