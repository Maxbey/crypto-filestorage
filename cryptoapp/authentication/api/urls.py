from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from .viewsets import UserSearchViewSet, GroupViewSet, PermissionViewSet

router = SimpleRouter()

router.register(r'group', GroupViewSet)
router.register(r'permission', PermissionViewSet)
router.register(r'user', UserSearchViewSet)

urlpatterns = [
    url(r'^', include(router.urls, namespace='auth-api')),
]
