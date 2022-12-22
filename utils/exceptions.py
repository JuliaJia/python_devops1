from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import PermissionDenied




class YunOpsBaseException(exceptions.APIException):
    code = 10000
    message = "未知错误，请联系管理员~！"

    @classmethod
    def get_message(cls):
        return {'code':cls.code,'message':cls.message}

class InvalidUserNameOrPassword(YunOpsBaseException):
    code = 1
    message = "用户名或密码错误"

exc_map = {
    'AuthenticationFailed': InvalidUserNameOrPassword,
}


def global_exception_handler(exc,context):
    response = exception_handler(exc,context)
    if response is not None:
        if isinstance(exc,YunOpsBaseException):
            errmessage = exc.get_message()
        else:
            errmessage = exc_map.get(exc.__class__.__name__,YunOpsBaseException).get_message()
        return Response(errmessage,status=200)
    return response

