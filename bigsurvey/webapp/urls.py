from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^site/(?P<pk>\d+)/$', views.SiteDetailView.as_view(), name="site_detail"),
    url(r'^site/add/$', views.SiteAddView.as_view(), name="site_add"),
    url(r'^site/(?P<pk>\d+)/edit/$', views.SiteEditView.as_view(), name="site_edit"),
    url(r'^pws/$', views.PWSView.as_view(), name="pws_list"),
    url(r'^pws/add/$', views.PWSAddView.as_view(), name="pws_add"),
    url(r'^pws/(?P<pk>\d+)/edit/$', views.PWSEditView.as_view(), name="pws_edit"),
    url(r'^customer/$', views.CustomerView.as_view(), name="customer_list"),
    url(r'^customer/(?P<pk>\d+)/$', views.CustomerDetailView.as_view(), name="customer_detail"),
    url(r'^customer/add/$', views.CustomerAddView.as_view(), name="customer_add"),
    url(r'^customer/(?P<pk>\d+)/edit/$', views.CustomerEditView.as_view(), name="customer_edit"),
    url(r'^survey/(?P<pk>\d+)/$', views.SurveyDetailView.as_view(), name="survey_detail"),
    url(r'^site/(?P<pk>\d+)/(?P<service>[a-z]+)/addsurvey/$', views.SurveyAddView.as_view(), name="survey_add"),
    url(r'^survey/(?P<pk>\d+)/edit/$', views.SurveyEditView.as_view(), name="survey_edit"),
    url(r'^hazard/(?P<pk>\d+)/$', views.HazardDetailView.as_view(), name="hazard_detail"),
    url(r'^survey/(?P<pk>\d+)/addhazard/$', views.HazardAddView.as_view(), name="hazard_add"),
    url(r'^hazard/(?P<pk>\d+)/edit/$', views.HazardEditView.as_view(), name="hazard_edit"),
)