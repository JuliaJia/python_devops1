from django.http.request import HttpRequest
from django.http.response import HttpResponse,HttpResponseNotAllowed,Http404,JsonResponse
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