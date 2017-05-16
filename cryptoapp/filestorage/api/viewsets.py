import base64

from django.conf import settings
from django.contrib.auth.models import Permission, Group
from django.db.models import Q

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Crypto.Cipher import AES

from authentication.permission import OwnerPermission
from .serializers import FileSerializer, FileDownloadSerializer, \
    FileGroupsSerializer

from ..models import File
from ..permissions import FileDecryptPermission, FileViewPermission


class FileUploadViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        filename = request.data.get('filename')
        file_content = request.data.get('file').read()
        salt = request.data.get('salt', None)

        original_content_length = len(file_content)

        if salt is None:
            raise ValidationError({'salt': 'This field is required.'})

        if not len(salt) == 16:
            raise ValidationError({'salt': 'Key length should be 16.'})

        if not original_content_length:
            raise ValidationError({'file': "Can't save an empty file."})

        whitespace_count = 16 - (len(file_content) % 16)
        file_content += (' ' * whitespace_count)

        aes = AES.new(salt, AES.MODE_CBC, settings.ENC_KEY)
        encrypted_content = aes.encrypt(file_content)
        content = base64.b64encode(encrypted_content)

        File.objects.create(
            user=request.user,
            name=filename,
            content=content,
            original_content_length=original_content_length
        )

        return Response({}, status.HTTP_201_CREATED)


class FileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, FileViewPermission]
    authentication_classes = [TokenAuthentication]

    serializer_class = FileSerializer
    queryset = File.objects.all()

    def filter_queryset(self, queryset):
        view_permission = Permission.objects.get(
            codename='view_file'
        )

        groups_view = Group.objects.filter(permissions__id__in=[
            view_permission.id
        ])

        return queryset.filter(
            Q(user=self.request.user) | Q(
                groups__id__in=[group.id for group in groups_view]
            )
        ).distinct()


class FileDecryptViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    serializer_class = FileDownloadSerializer
    queryset = File.objects.all()

    def create(self, request, *args, **kwargs):
        request_serializer = self.get_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        file = request_serializer.validated_data['file']
        salt = request_serializer.validated_data['salt']

        permission = FileDecryptPermission()

        if not permission.has_object_permission(self.request, self, file):
            raise PermissionDenied()

        aes = AES.new(salt, AES.MODE_CBC, settings.ENC_KEY)
        content = base64.b64decode(file.content)
        decrypted_content = aes.decrypt(content)

        return Response(
            {'file': decrypted_content[:file.original_content_length]}
        )


class FileGroupsViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, OwnerPermission]
    authentication_classes = [TokenAuthentication]

    serializer_class = FileGroupsSerializer
    queryset = File.objects.all()

    paginator = None
