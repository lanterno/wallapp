from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from django.views.generic import RedirectView

from wallapp.core.views import SwaggerSchemaView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(pattern_name='docs', permanent=True), name='index'),
    url(r'^api/v1/docs/$', SwaggerSchemaView.as_view(), name='docs'),
    url(r'^api/v1/users/', include('wallapp.accounts.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = 'WallApp Administration'
admin.site.site_title = 'WallApp'
