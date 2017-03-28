from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^disable-account/$', views.SuspendAccountView.as_view(), name='disable_account'),
    url(r'^', include('djoser.urls.authtoken')),
]
