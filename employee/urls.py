from django.urls import path
from django.views.decorators.http import require_GET
from rest_framework.routers import SimpleRouter

from .views import test_index, TestView, cookieView, serializeView, TestAPIView, EmpView, SalaryView, EmpsView, \
    EmpViewSet


router = SimpleRouter()

router.register('',EmpViewSet)

urlpatterns = [
    path('test6/',test_index),
    path('test/',require_GET(TestView.as_view())),
    path('test2/',cookieView),
    path('test3/',serializeView),
    path('test4/',TestAPIView.as_view()),
    # path('<int:pk>',EmpViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
    # path('',EmpViewSet.as_view({'get':'list','post':'create'})),
    path('salary/<int:pk>',SalaryView.as_view()),

] + router.urls