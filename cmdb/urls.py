from django.urls import path
from .views import CiTypeViewSet,CiViewSet,CiWithIdViewSet
from rest_framework.routers import SimpleRouter

# from .views import menulist_view, UserViewSet, PermViewSet, RoleViewSet, User2ViewSet

router = SimpleRouter()
router.register(r'citypes',CiTypeViewSet,'citypes')
router.register(r"cis", CiViewSet,'cis')
router.register(r"cisid", CiWithIdViewSet,'cisid')
# router.register("userroles", User2ViewSet)
urlpatterns = [
    path('<int:pk>',CiTypeViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
    path('<int:pk>', CiWithIdViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    # path('citypes/',CiTypeViewSet.as_view()),
    # path('<int:pk>',UserViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
    # path('perms/', PermViewSet.as_view({'get': 'list'})),
    # path('perms/<int:pk>', PermViewSet.as_view({'get': 'retrieve'})),
    # # path('roles/', RoleViewSet.as_view({'get': 'list','post':'create'})),
    # # path('roles/<int:pk>/perms/', RoleViewSet.as_view({'get': 'retrieve'})),
    # # path('userroles/<int:pk>', UserViewSet.as_view({'get': 'list','post':'create'})),
    # path('<int:pk>/', RoleViewSet.as_view({'get': 'retrieve','put':'update','patch':'partial_update','delete':'destroy'})),
] + router.urls