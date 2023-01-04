from rest_framework.permissions import DjangoModelPermissions
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.contrib.auth.models import Permission
import sys
sys.path.append("..")
from user.models import UserProfile


class CrudModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsCMDBer(BasePermission):
    def has_permission(self,request:Request,view):
        # print(request.user.has_perm('cmdb.can_citypes'))
        # user = UserProfile.objects.get(username=request.user.username)
        # print(request.user.has_perm('cmdb.can_citype'))
        return True if request.user.has_perm('cmdb.can_citype') else False
