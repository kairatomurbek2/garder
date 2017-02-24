from django.conf.urls import patterns, include, url, static
from django.views.generic import TemplateView
from webapp.admin import admin_site_bigsurvey
from django.conf import settings
from ajax_select import urls as ajax_select_urls
from webapp.forms import EmailValidationOnForgotPassword

urlpatterns = patterns(
    '',
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^admin/', include(admin_site_bigsurvey.urls)),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^', include('webapp.urls', namespace='webapp')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': 'done/',
         'password_reset_form': EmailValidationOnForgotPassword}, name="password_reset"),
    url(r'^password/reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^password/reset/complete$', 'django.contrib.auth.views.password_reset_complete',
        name="password_reset_complete"),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': 'password_reset_complete'}, name='password_reset_activation'),
    (r'^404/$', TemplateView.as_view(template_name="404.html")),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
