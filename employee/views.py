import random

import json
from django.contrib.sessions.models import Session
from django.http.request import HttpRequest
from django.http.response import HttpResponse,HttpResponseNotAllowed,Http404,JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET,require_POST,require_http_methods



# @require_GET
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView,Request,Response
from rest_framework.viewsets import ModelViewSet

from .models import Employee, Salary
from .serializers import EmpSerializer, EmpSerializerModel, SalarySerializerModel


@require_http_methods(['GET','POST'])
def test_index(request):
    # return HttpResponse("xyz")
    return JsonResponse({"1":[1,2,3]},status=204)
    # if request.method.lower() == 'get':
    #     return JsonResponse({"1":[1,2,3]},status=204)
    # else:
    #     return HttpResponseNotAllowed(["GET"])



class MyMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        print(self.__class__.__name__,'init~~~~~~~')
    def __call__(self,request):
        print(self.__class__.__name__, 'response之前~~~~~~~')
        response = self.get_response(request)
        print(self.__class__.__name__, 'response之后~~~~~~~')
        return response
    def process_view(self,request,view_func,view_args,view_kwargs):
        print(self.__class__.__name__,view_func,view_args,view_kwargs)
        # return HttpResponse("test")


class TestView(View):

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request):
        print("我是Get，我被调用了！")
        return JsonResponse({"2":[4,5,6]},status=200)


    def post(self,request):
        print("我是Post，我被调用了！")
        return JsonResponse({"3":[7,8,9]},status=200)
        # return HttpResponseNotAllowed(["GET"])



def cookieView(request:HttpRequest):
    print(request.COOKIES)
    # res = JsonResponse({"3":[7,8,9]},status=200)
    res = HttpResponse('123')
    res.cookies["1"] = 'A1'
    sessionKey = request.COOKIES["sessionid"]
    sessionValue = str(random.randint(100,200))
    request.session["session1"] = sessionValue
    s = Session.objects.get(pk=sessionKey)
    print(s.get_decoded())
    return res

def serializeView(request:HttpRequest):
    d = {
        'emp_no':10012,
        'birth_date': '2000-01-01',
        'first_name': 'tian',
        'last_name': 'cai3',
        'gender': 1,
        'hire_date': '2020-02-02',
    }

    #查询
    emgr = Employee.objects
    emp = emgr.filter(pk__gt=10000)
    serializer = EmpSerializerModel(instance=emp,many=True)
    print(serializer.data)
    res = HttpResponse(json.dumps(serializer.data))

    #update
    # emp = emgr.get(pk=10012)
    # serializer = EmpSerializerModel(instance=emp, data=d)
    # x = serializer.is_valid(raise_exception=True)
    # if x == True:
    #     serializer.save()
    # res = JsonResponse(serializer.validated_data)

    # emgr = Employee.objects
    # emp = emgr.get(pk=10012)
    # serializer = EmpSerializer(emp,data=d)
    # x = serializer.is_valid(raise_exception=True) #依赖序列化器校验
    # print(x)
    # if x == True:
    #     serializer.save()
    # res = JsonResponse(serializer.validated_data)
    # x = serializer.validate_first_name(d["first_name"])
    # res = HttpResponse(x)


    #这段是从数据库获取信息
    # emgr = Employee.objects
    # emp = emgr.get(pk=10010)
    # emp.test1 = 1000000
    # serializer2 = EmpSerializer(instance=emp)
    # res2 = JsonResponse(serializer2.data)
    return res

class TestAPIView(APIView):
    def get(self,request:Request):
        print(1,type(request))
        print(2,isinstance(request,HttpRequest))
        print(3,request.content_type)
        print(4,request.method)
        print(5,request.query_params)
        print(6,request.GET)
        return Response({'test':[1,'abc']},201)
    def post(self,request:Request):
        print(11,request.method)
        print(12,request.content_type)
        print(13,request.query_params)
        print(14,request.body)
        return Response({"method":request.method})


class EmpViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmpSerializerModel
    pagination_class = LimitOffsetPagination
    # lookup_url_kwarg = 'pk'


class EmpView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmpSerializerModel
    pagination_class = LimitOffsetPagination


class EmpsView(ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmpSerializerModel
    pagination_class = LimitOffsetPagination



class EmpView2(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmpSerializerModel
    pagination_class = LimitOffsetPagination
    # def get_queryset(self):
    #     return super().get_queryset.filter(pk__gt=10000)
    #
    # def get_serializer_class(self):
    #     return SalarySerializerModel

    get = RetrieveModelMixin.retrieve
    put = UpdateModelMixin.update
    patch = UpdateModelMixin.partial_update
    delete = DestroyModelMixin.destroy

class EmpsView2(CreateModelMixin,ListModelMixin,GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmpSerializerModel
    pagination_class = LimitOffsetPagination
    # def get(self,request,*args,**kwargs):
    #     return super().list(request,*args,**kwargs)
    # def post(self,requst,*args,**kwargs):
    #     return super().create(requst,*args,**kwargs)

    #更好的方式
    get = ListModelMixin.list
    post = CreateModelMixin.create

class SalaryView(GenericAPIView):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializerModel




class EmpView1(APIView):
    def get(self,request,pk:int):
        obj = Employee.objects.get(pk=pk)
        return Response(EmpSerializerModel(obj).data)

    def put(self,request,pk:int):
        obj = Employee.objects.get(pk=pk)
        serializer = EmpSerializerModel(instance=obj,data=request.data)
        x = serializer.is_valid(raise_exception=True)
        print(x)
        serializer.save()
        return Response(serializer.data,201)
    def delete(self,request,pk:int):
        obj = Employee.objects.get(pk=pk)
        obj.delete()
        return Response(status=204)


class SalaryView1(APIView):
    def get(self,request,pk:int):
        obj = Salary.objects.get(pk=pk)
        return Response(SalarySerializerModel(obj).data)

    def put(self,request,pk:int):
        obj = Salary.objects.get(pk=pk)
        serializer = SalarySerializerModel(instance=obj,data=request.data)
        x = serializer.is_valid(raise_exception=True)
        print(x)
        serializer.save()
        return Response(serializer.data,201)
    def delete(self,request,pk:int):
        obj = Salary.objects.get(pk=pk)
        obj.delete()
        return Response(status=204)