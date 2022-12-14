from django.http.request import HttpRequest
from django.http.response import HttpResponse,HttpResponseNotAllowed,Http404,JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_GET,require_POST,require_http_methods



# @require_GET
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

