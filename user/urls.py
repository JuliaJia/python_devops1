from django.urls import path
from django.views.decorators.http import require_GET
from rest_framework.routers import SimpleRouter

from .views import menulist_view

urlpatterns = [
    path('menulist/',menulist_view),
]