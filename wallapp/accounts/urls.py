from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^disable-account/$', views.SuspendAccountView.as_view(), name='disable_account'),
    url(r'^activate/$', views.ActivationView.as_view(), name='activate'),
    url(r'^', include('djoser.urls.authtoken')),
]
