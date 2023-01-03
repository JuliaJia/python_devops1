
from django.contrib.auth import authenticate, login, logout, get_user_model

# Create your views here.
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import UserSerializer, PermSerializer, GroupSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from utils.exceptions import InvalidPassword

_exclude_contenttypes = [c.id for c in ContentType.objects.filter(model__in=[
    'logentry', 'group', 'permission', 'contenttype', 'session'
])]


@api_view(['POST','GET'])
def test(request:Request):
    print(request.COOKIES, request._request.headers)
    print(request.user)
    print(request.data)
    print(request.auth)
    if request.auth:
        return Response({'test':10000})
    else:
        return Response({'test':20000})


class PermViewSet(ReadOnlyModelViewSet):
    queryset = Permission.objects.exclude(content_type__in=_exclude_contenttypes)
    serializer_class = PermSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'codename']

class RoleViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['name']

    @action(['GET'],detail=True,url_path='perms')
    def get_perms(self, request, pk):
        obj = self.get_object()
        data = GroupSerializer(obj).data
        data['allPerms'] = list(PermViewSet.queryset.values('id', 'name'))
        return Response(data)

    def get_queryset(self):
        queryset = super().get_queryset()
        rolename = self.request.query_params.get('rolename', None)
        if rolename:
            queryset = queryset.filter(name__icontains=rolename)
        return queryset


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated | IsAdminUser] # or
    filter_backends = [filters.SearchFilter]
    # filterset_fields = ['username']
    search_fields = ["username"]
    
    def partial_update(self, request, *args, **kwargs):
        request.data.pop('username', None)
        request.data.pop('id', None)
        request.data.pop('password', None)
        return super().partial_update(request,*args, **kwargs)

    def get_object(self,status=None):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == 1 or pk == '1':
                if status == None:
                    raise Http404
                else:
                    return super().get_object()
        return super().get_object()
    @action(['GET'], detail=False, url_path='whoami')
    def whoami(self,request):
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username
            }
        })
    @action(detail=True, methods=['post'], url_path='setpwd' )
    def set_password(self, request, pk=None):
        user = self.get_object(1)
        if user.check_password(request.data["oldPassword"]):
            print("test")
            user.set_password(request.data["password"])
            user.save()
            return Response()
        else:
            raise InvalidPassword

    @action(detail=True, methods=['GET'], url_path='roles')
    def roles(self, request, pk=None):
        user = self.get_object()
        data = UserSerializer(user).data
        data['roles'] = [r.get('id') for r in user.groups.values('id')]
        data['allRoles'] = Group.objects.values('id', 'name')
        return Response(data)

    @roles.mapping.put
    def set_roles(self, request, pk=None):
        user = self.get_object()
        roles = request.data.get('roles', [])
        user.groups.set(roles)
        return Response(status=201)


    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset


class User2ViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    # filterset_fields = ['username']
    search_fields = ["username"]

    def partial_update(self, request, *args, **kwargs):
        request.data.pop('username', None)
        request.data.pop('id', None)
        request.data.pop('password', None)
        return super().partial_update(request, *args, **kwargs)

    def get_object(self, status=None):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == 1 or pk == '1':
                if status == None:
                    raise Http404
                else:
                    return super().get_object()
        return super().get_object()

    @action(['GET'], detail=False, url_path='whoami')
    def whoami(self, request):
        return Response({
            'user': {
                'id': request.user.id,
                'username': request.user.username
            }
        })

    @action(detail=True, methods=['post'], url_path='setpwd')
    def set_password(self, request, pk=None):
        user = self.get_object(1)
        if user.check_password(request.data["oldPassword"]):
            print("test")
            user.set_password(request.data["password"])
            user.save()
            return Response()
        else:
            raise InvalidPassword

    @action(detail=True, methods=['GET'], url_path='roles')
    def roles(self, request, pk=None):
        user = self.get_object()
        data = UserSerializer(user).data
        data['roles'] = [r.get('id') for r in user.groups.values('id')]
        data['allRoles'] = Group.objects.values('id', 'name')
        return Response(data)

    @roles.mapping.put
    def set_roles(self, request, pk=None):
        user = self.get_object()
        roles = request.data.get('roles', [])
        user.groups.set(roles)
        return Response(status=201)

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username', None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

class MenuItem(dict):
    def __init__(self,id,name,path=None):
        super().__init__()
        self["id"] = id
        self["name"] = name
        self["path"] = path
        self["children"] =[]
    def append(self,item):
        self["children"].append(item)

@api_view(['GET'])
@permission_classes([IsAuthenticated | IsAdminUser])
def menulist_view(request:Request):
    menulist = []
    if request.user.is_superuser:
        item = MenuItem(1,'用户管理')
        item.append(MenuItem(101,'用户列表','/users'))
        item.append(MenuItem(102, '角色列表', '/users/roles'))
        item.append(MenuItem(103, '权限列表', '/users/perms'))
        menulist.append(item)
    print(menulist)
    return Response(menulist)