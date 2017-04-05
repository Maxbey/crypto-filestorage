from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from .viewsets import UserSearchViewSet, UserGroupsViewSet, GroupViewSet

router = SimpleRouter()

router.register(r'group', GroupViewSet)
router.register(r'user', UserSearchViewSet)
router.register(r'user/group', UserGroupsViewSet)

urlpatterns = [
    url(r'^', include(router.urls, namespace='auth-api')),
]
