from django.urls import path
from .views import test_index
urlpatterns = [
    path('',test_index),
]