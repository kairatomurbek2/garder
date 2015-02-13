from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^site/(?P<pk>\d+)/$', views.SiteDetailView.as_view(), name="site_detail"),
    url(r'^site/add/$', views.SiteAddView.as_view(), name="site_add"),
    url(r'^site/(?P<pk>\d+)/edit/$', views.SiteEditView.as_view(), name="site_edit"),
    url(r'^inspection/$', views.InspectionListView.as_view(), name="inspection_list"),
    url(r'^site/(?P<pk>\d+)/assign/$', views.InspectionAddView.as_view(), name="inspection_add"),
    url(r'^inspection/(?P<pk>\d+)/edit/$', views.InspectionEditView.as_view(), name="inspection_edit"),
    url(r'^testpermission/$', views.TestPermissionListView.as_view(), name="testpermission_list"),
    url(r'^site/(?P<pk>\d+)/grant/$', views.TestPermissionAddView.as_view(), name="testpermission_add"),
    url(r'^testpermission/(?P<pk>\d+)/edit$', views.TestPermissionEditView.as_view(), name="testpermission_edit"),
    url(r'^pws/$', views.PWSListView.as_view(), name="pws_list"),
    url(r'^pws/add/$', views.PWSAddView.as_view(), name="pws_add"),
    url(r'^pws/(?P<pk>\d+)/edit/$', views.PWSEditView.as_view(), name="pws_edit"),
    url(r'^customer/$', views.CustomerListView.as_view(), name="customer_list"),
    url(r'^customer/(?P<pk>\d+)/$', views.CustomerDetailView.as_view(), name="customer_detail"),
    url(r'^customer/add/$', views.CustomerAddView.as_view(), name="customer_add"),
    url(r'^customer/(?P<pk>\d+)/edit/$', views.CustomerEditView.as_view(), name="customer_edit"),
    url(r'^survey/(?P<pk>\d+)/$', views.SurveyDetailView.as_view(), name="survey_detail"),
    url(r'^site/(?P<pk>\d+)/(?P<service>[a-z]+)/addsurvey/$', views.SurveyAddView.as_view(), name="survey_add"),
    url(r'^survey/(?P<pk>\d+)/edit/$', views.SurveyEditView.as_view(), name="survey_edit"),
    url(r'^hazard/(?P<pk>\d+)/$', views.HazardDetailView.as_view(), name="hazard_detail"),
    url(r'^survey/(?P<pk>\d+)/addhazard/$', views.HazardAddView.as_view(), name="hazard_add"),
    url(r'^hazard/(?P<pk>\d+)/edit/$', views.HazardEditView.as_view(), name="hazard_edit"),
    url(r'^hazard/(?P<pk>\d+)/addtest/$', views.TestAddView.as_view(), name="test_add"),
    url(r'^test/(?P<pk>\d+)/edit/$', views.TestEditView.as_view(), name="test_edit"),
    url(r'^user/$', views.UserListView.as_view(), name="user_list"),
    url(r'^user/add/$', views.UserAddView.as_view(), name="user_add"),
    url(r'^user/(?P<pk>\d+)/edit/$', views.UserEditView.as_view(), name="user_edit"),
)