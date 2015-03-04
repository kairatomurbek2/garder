from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^', include('webapp.urls', namespace='webapp')),
    url(r'^redactor/', include('redactor.urls'))
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
