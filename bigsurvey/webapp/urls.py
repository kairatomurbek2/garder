from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^site/(?P<pk>\d+)/$', views.SiteDetailView.as_view(), name="site_detail"),
    url(r'^site/add/$', views.SiteAddView.as_view(), name="site_add"),
    url(r'^site/edit/(?P<pk>\d+)/$', views.SiteEditView.as_view(), name="site_edit"),
    url(r'^pws/$', views.PWSView.as_view(), name="pws_list"),
    url(r'^pws/add/$', views.PWSAddView.as_view(), name="pws_add"),
    url(r'^pws/edit/(?P<pk>\d+)/$', views.PWSEditView.as_view(), name="pws_edit"),
    url(r'^customer/$', views.CustomerView.as_view(), name="customer_list"),
    url(r'^customer/(?P<pk>\d+)/$', views.CustomerDetailView.as_view(), name="customer_detail"),
    url(r'^customer/add/$', views.CustomerAddView.as_view(), name="customer_add"),
    url(r'^customer/edit/(?P<pk>\d+)/$', views.CustomerEditView.as_view(), name="customer_edit"),
)
