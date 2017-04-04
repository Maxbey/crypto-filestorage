from django.conf.urls import url, include
from django.contrib import admin

from rest_auth.views import LoginView, LogoutView

from authentication.api.viewsets import RegisterViewSet

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(
        r'^api/auth/register/$',
        RegisterViewSet.as_view(),
        name='rest_register'
    ),
    url(r'^api/auth/login/$', LoginView.as_view(), name='rest_login'),
    url(r'^api/auth/logout/$', LogoutView.as_view(), name='rest_logout'),

    url(
        r'^api/auth/',
        include('authentication.api.urls', namespace='authentication_api')
    ),
]
