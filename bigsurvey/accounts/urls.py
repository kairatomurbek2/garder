from django.conf.urls import url, patterns

urlpatterns = patterns('accounts.views',

    url(r'^login/', 'login', {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/', 'logout_view', name='logout'),

)

