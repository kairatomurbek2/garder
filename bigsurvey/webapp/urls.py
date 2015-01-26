from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^site/(?P<pk>\d+)/$', views.SiteDetailView.as_view(), name="site_detail"),
    url(r'^pws/$', views.PWSView.as_view(), name="pws_list"),
    url(r'^pws/add/$', views.PWSAddView.as_view(), name="pws_add"),
    url(r'^pws/edit/(?P<pk>\d+)/$', views.PWSEditView.as_view(), name="pws_edit"),
)
