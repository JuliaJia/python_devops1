from django.contrib.auth import authenticate,login,logout

# Create your views here.
from django.http import HttpResponse
from rest_framework.decorators import api_view
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
