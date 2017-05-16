from django.conf import settings
from django.contrib.auth.models import User, Group, Permission

from rest_auth.app_settings import create_token
from rest_auth.registration.views import RegisterView
from rest_auth.utils import jwt_encode
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import list_route
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..permission import OwnerPermission
from .serializers import RegisterSerializer, UserSerializer, \
    GroupSerializer, PermissionSerializer


class RegisterViewSet(RegisterView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)

        return user


class UserSearchViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = User.objects.all()

    paginator = None

    def filter_queryset(self, queryset):
        if 'username' not in self.request.data:
            return User.objects.all()

        username = self.request.data['username']

        return User.objects.filter(username__startswith=username)

    @list_route(methods=['post'])
    def search(self, request):
        filtered = self.filter_queryset(self.queryset)

        return Response(UserSerializer(filtered, many=True).data)


class GroupViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, OwnerPermission]
    authentication_classes = [TokenAuthentication]

    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    paginator = None

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)


class PermissionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()

