from django.urls import path
from django.views.decorators.http import require_GET

from .views import test_index, TestView

urlpatterns = [
    path('',test_index),
    path('test/',require_GET(TestView.as_view())),
    path('test2/',TestView.as_view()),
]