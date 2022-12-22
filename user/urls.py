from django.urls import path
from django.views.decorators.http import require_GET
from rest_framework.routers import SimpleRouter

from .views import menulist_view, UserViewSet

router = SimpleRouter()
router.register("",UserViewSet)


urlpatterns = [
    path('menulist/',menulist_view),
path('<int:pk>',UserViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
] + router.urls