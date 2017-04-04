from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from .viewsets import UserSearchViewSet, AddUserToGroupViewSet, \
    GroupViewSet, RemoveUserFromGroupsViewSet

router = SimpleRouter()

router.register(r'group', GroupViewSet)
router.register(r'user', UserSearchViewSet)
router.register(r'group/add_user', AddUserToGroupViewSet)
router.register(r'group/remove_user', RemoveUserFromGroupsViewSet)

urlpatterns = [
    url(r'^', include(router.urls, namespace='auth-api')),
]
