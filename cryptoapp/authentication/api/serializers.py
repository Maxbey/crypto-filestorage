import phonenumbers
from authy import AuthyException

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField
from rest_auth.serializers import LoginSerializer as BaseLoginSerializer, \
    UserModel
from rest_framework import exceptions
from rest_framework import serializers

from rest_auth.registration.serializers import \
    RegisterSerializer as BaseRegisterSerializer

from ..two_factor_auth import AuthyProvider


class RegisterSerializer(BaseRegisterSerializer):
    cellphone = serializers.CharField(
        validators=PhoneNumberField().validators
    )

    def custom_signup(self, request, user):
        cellphone = phonenumbers.parse(request.data['cellphone'], None)
        provider = AuthyProvider(user)

        return provider.register_user(cellphone)


class LoginSerializer(BaseLoginSerializer):
    authy_token = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                user = self._validate_email(email, password)

            # Authentication through username
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                user = self._validate_username(username, password)

            # Authentication through either username or email
            else:
                user = self._validate_username_email(username, email, password)

        else:
            # Authentication without using allauth
            if email:
                try:
                    username = UserModel.objects.get(
                        email__iexact=email).get_username()
                except UserModel.DoesNotExist:
                    pass

            if username:
                user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    raise serializers.ValidationError(
                        _('E-mail is not verified.'))

        provider = AuthyProvider(user)
        try:
            if not provider.verify_token(attrs['authy_token']):
                raise exceptions.ValidationError({
                    'authy_token': 'Token is invalid.'
                })
        except AuthyException:
            raise exceptions.ValidationError({
                'authy_token': 'Token is invalid.'
            })

        attrs['user'] = user
        return attrs


class GroupSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Group
        fields = [
            'id',
            'name'
        ]


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        read_only=True, many=True
    )

    class Meta(object):
        model = get_user_model()
        fields = [
            'id',
            'username',
            'groups'
        ]


class UserGroupsSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects, write_only=True
    )
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects, write_only=True, many=True
    )

    def create(self, validated_data):
        user = validated_data.get('user')
        groups = validated_data.get('groups')

        user.groups.set(groups)
        user.save()

        return user
