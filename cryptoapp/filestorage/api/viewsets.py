import base64

from django.conf import settings

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Crypto.Cipher import AES

from .serializers import FileSerializer, FileDownloadSerializer
from ..models import File


class FileUploadViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        filename = request.data.get('filename')
        file = request.data.get('file').read()
        salt = request.data.get('salt', None)

        if salt is None:
            raise ValidationError({'salt': 'This field is required.'})

        if not len(salt) == 16:
            raise ValidationError({'salt': 'Key length should be 16'})

        aes = AES.new(salt, AES.MODE_CBC, settings.ENC_KEY)
        encrypted_content = aes.encrypt(file)
        content = base64.b64encode(encrypted_content)

        File.objects.create(
            user=request.user,
            name=filename,
            content=content
        )

        return Response({}, status.HTTP_201_CREATED)


class FileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    serializer_class = FileSerializer
    queryset = File.objects.all()

    def filter_queryset(self, queryset):
        if self.request.user.has_perm('auth.observe_private_access'):
            return queryset

        return queryset.filter(user=self.request.user)


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

        aes = AES.new(salt, AES.MODE_CBC, settings.ENC_KEY)
        content = base64.b64decode(file.content)
        decrypted_content = aes.decrypt(content)

        return Response({'file': decrypted_content})
