from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from .viewsets import FileViewSet, FileUploadViewSet, FileDecryptViewSet, \
    FileGroupsViewSet

router = SimpleRouter()

router.register(r'file', FileViewSet)
router.register(r'file/group', FileGroupsViewSet)
router.register(r'upload', FileUploadViewSet, base_name='upload_file')
router.register(r'decrypt', FileDecryptViewSet, base_name='decrypt_file')

urlpatterns = [
    url(r'^', include(router.urls, namespace='storage-api')),
]
