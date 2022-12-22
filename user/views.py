from django.contrib.auth import authenticate,login,logout

# Create your views here.
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response




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