from django.contrib.auth import authenticate, login, logout, get_user_model

# Create your views here.
from django.http import HttpResponse, Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


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


class UserViewSet(ModelViewSet):
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
        return super().partial_update(request,*args, **kwargs)

    def get_object(self):
        if self.request.method.lower() != 'get':
            pk = self.kwargs.get('pk')
            if pk == 1 or pk == '1':
                raise Http404
        return super().get_object()

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
@permission_classes([IsAuthenticated,IsAdminUser])
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