from django.conf.urls import patterns, url

from webapp import views


urlpatterns = patterns(
    '',
    url(r'^$', views.HomeView.as_view(), name="home"),
    url(r'^tester-home/$', views.TesterHomeView.as_view(), name="tester-home"),
    url(r'^site/add/$', views.SiteAddView.as_view(), name="site_add"),
    url(r'^site/(?P<pk>\d+)/$', views.SiteDetailView.as_view(), name="site_detail"),
    url(r'^site/(?P<pk>\d+)/edit/$', views.SiteEditView.as_view(), name="site_edit"),
    url(r'^site/(?P<pk>\d+)/add-letter/$', views.LetterAddView.as_view(), name="letter_add"),
    url(r'^site/(?P<pk>\d+)/(?P<service>[a-z]+)/add-survey/$', views.SurveyAddView.as_view(), name="survey_add"),
    url(r'^site/(?P<pk>\d+)/(?P<service>[a-z]+)/add-hazard/$', views.HazardAddView.as_view(), name="hazard_add"),

    url(r'^batch_update/$', views.BatchUpdateView.as_view(), name='batch_update'),

    url(r'^survey/$', views.SurveyListView.as_view(), name="survey_list"),
    url(r'^survey/(?P<pk>\d+)/$', views.SurveyDetailView.as_view(), name="survey_detail"),
    url(r'^survey/(?P<pk>\d+)/edit/$', views.SurveyEditView.as_view(), name="survey_edit"),

    url(r'^hazard/$', views.HazardListView.as_view(), name="hazard_list"),
    url(r'^hazard/(?P<pk>\d+)/$', views.HazardDetailView.as_view(), name="hazard_detail"),
    url(r'^hazard/(?P<pk>\d+)/edit/$', views.HazardEditView.as_view(), name="hazard_edit"),
    url(r'^hazard/(?P<pk>\d+)/add-test/$', views.TestAddView.as_view(), name="test_add"),

    url(r'^test/$', views.TestListView.as_view(), name="test_list"),
    url(r'^unpaid-test/$', views.UnpaidTestListView.as_view(), name="unpaid_test_list"),
    url(r'^test/(?P<pk>\d+)/edit/$', views.TestEditView.as_view(), name="test_edit"),
    url(r'^testers/$', views.TesterListView.as_view(), name="tester_list"),

    url(r'^letter/$', views.LetterListView.as_view(), name="letter_list"),
    url(r'^letter/(?P<pk>\d+)/$', views.LetterDetailView.as_view(), name="letter_detail"),
    url(r'^letter/(?P<pk>\d+)/edit/$', views.LetterEditView.as_view(), name="letter_edit"),
    url(r'^letter/(?P<pk>\d+)/pdf/$', views.LetterPDFView.as_view(), name="letter_pdf"),

    url(r'^pws/$', views.PWSListView.as_view(), name="pws_list"),
    url(r'^pws/add/$', views.PWSAddView.as_view(), name="pws_add"),
    url(r'^pws/(?P<pk>\d+)/edit/$', views.PWSEditView.as_view(), name="pws_edit"),

    url(r'^user/$', views.UserListView.as_view(), name="user_list"),
    url(r'^user/add/$', views.UserAddView.as_view(), name="user_add"),
    url(r'^user/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name="user_detail"),
    url(r'^user/(?P<pk>\d+)/edit/$', views.UserEditView.as_view(), name="user_edit"),

    url(r'^import/$', views.ImportView.as_view(), name="import"),
    url(r'^import-mappings/$', views.ImportMappingsRenderView.as_view(), name="import-mappings"),
    url(r'^import-mappings-process/$', views.ImportMappingsProcessView.as_view(), name="import-mappings-process"),
    url(r'^import-progress/$', views.ImportProgressView.as_view(), name="import-progress"),

    url(r'^help/$', views.HelpView.as_view(), name="help"),
)