from django.conf import settings
from django.contrib.auth.models import User, Group

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

from authentication.permissions import CanManageUserPermissions
from .serializers import RegisterSerializer, UserSerializer, \
    GroupSerializer, UserGroupsSerializer


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
    permission_classes = [IsAuthenticated, CanManageUserPermissions]
    authentication_classes = [TokenAuthentication]

    queryset = User.objects.all()

    paginator = None

    def filter_queryset(self, queryset):
        username = self.request.data['username']

        return User.objects.filter(username__startswith=username)

    @list_route(methods=['post'])
    def search(self, request):
        if 'username' not in request.data:
            raise ValidationError(
                {'username': 'This field is required.'}
            )

        filtered = self.filter_queryset(self.queryset)

        return Response(UserSerializer(filtered, many=True).data)


class GroupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, CanManageUserPermissions]
    authentication_classes = [TokenAuthentication]

    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    paginator = None


class UserGroupsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, CanManageUserPermissions]
    authentication_classes = [TokenAuthentication]

    serializer_class = UserGroupsSerializer
    queryset = User.objects.all()

    paginator = None

