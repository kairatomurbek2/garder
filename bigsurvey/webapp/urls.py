from auditlog.views import AuditLogView
from django.conf.urls import patterns, url
from forms import PasswordChangeWithMinLengthForm
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

    url(r'^batch_update/$', views.BatchUpdateView.as_view(), name='batch_update'),

    url(r'^survey/$', views.SurveyListView.as_view(), name="survey_list"),
    url(r'^survey/(?P<pk>\d+)/$', views.SurveyDetailView.as_view(), name="survey_detail"),
    url(r'^survey/(?P<pk>\d+)/edit/$', views.SurveyEditView.as_view(), name="survey_edit"),

    url(r'^hazard/$', views.HazardListView.as_view(), name="hazard_list"),
    url(r'^hazard/(?P<pk>\d+)/$', views.HazardDetailView.as_view(), name="hazard_detail"),
    url(r'^hazard/(?P<pk>\d+)/edit/$', views.HazardEditView.as_view(), name="hazard_edit"),

    url(r'^test/$', views.TestListView.as_view(), name="test_list"),
    url(r'^test/(?P<pk>\d+)/$', views.TestDetailView.as_view(), name="test_detail"),
    url(r'^unsaved-tests/$', views.UnpaidTestView.as_view(), name="unpaid_test_list"),
    url(r'^test/(?P<pk>\d+)/edit/$', views.TestEditView.as_view(), name="test_edit"),
    url(r'^test/pay/paypal/$', views.TestPayPaypalView.as_view(), name="test_pay_paypal"),
    url(r'^testers/$', views.TesterListView.as_view(), name="tester_list"),
    url(r'^user-search/$', views.UserSearchView.as_view(), name="user_search"),
    url(r'^invite-accept/$', views.UserInviteAcceptView.as_view(), name="invite_accept"),

    url(r'^letter_type/$', views.LetterTypeListView.as_view(), name="letter_type_list"),
    url(r'^letter_type/(?P<pk>\d+)/edit/$', views.LetterTypeEditView.as_view(), name="letter_type_edit"),

    url(r'^letter/$', views.LetterListView.as_view(), name="letter_list"),
    url(r'^letter/(?P<pk>\d+)/$', views.LetterDetailView.as_view(), name="letter_detail"),
    url(r'^letter/(?P<pk>\d+)/edit/$', views.LetterEditView.as_view(), name="letter_edit"),
    url(r'^letter/(?P<pk>\d+)/pdf/$', views.LetterPDFView.as_view(), name="letter_pdf"),

    url(r'^pws/$', views.PWSListView.as_view(), name="pws_list"),
    url(r'^pws/(?P<pk>\d+)/$', views.PWSDetailView.as_view(), name="pws_detail"),
    url(r'^pws/add/$', views.PWSAddView.as_view(), name="pws_add"),
    url(r'^pws/(?P<pk>\d+)/edit/$', views.PWSEditView.as_view(), name="pws_edit"),
    url(r'^pws/(?P<pk>\d+)/snapshot/$', views.SnapshotView.as_view(), name="pws_snapshot"),

    url(r'^user/$', views.UserListView.as_view(), name="user_list"),
    url(r'^user/add/$', views.UserAddView.as_view(), name="user_add"),
    url(r'^user/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name="user_detail"),
    url(r'^user/(?P<pk>\d+)/edit/$', views.UserEditView.as_view(), name="user_edit"),

    url(r'^import/$', views.ImportView.as_view(), name="import"),
    url(r'^import-mappings/$', views.ImportMappingsRenderView.as_view(), name="import-mappings"),
    url(r'^import-mappings-process/$', views.ImportMappingsProcessView.as_view(), name="import-mappings-process"),
    url(r'^import-progress/$', views.ImportProgressView.as_view(), name="import-progress"),

    url(r'^import-log/$', views.ImportLogListView.as_view(), name="import_log_list"),
    url(r'^import-log/(?P<pk>\d+)/added/$', views.ImportLogAddedSitesView.as_view(), name="import_log_added_sites"),
    url(r'^import-log/(?P<pk>\d+)/updated/$', views.ImportLogUpdatedSitesView.as_view(), name="import_log_updated_sites"),
    url(r'^import-log/(?P<pk>\d+)/deactivated/$', views.ImportLogDeactivatedSitesView.as_view(), name="import_log_deactivated_sites"),

    url(r'^help/$', views.HelpView.as_view(), name="help"),
    url(r'^get_test_kits/(?P<tester_id>\d+)/', views.get_test_kits, name='get_kits'),
    url(r'^get_tester_certs/(?P<tester_id>\d+)/', views.get_tester_certs, name='get_certs'),

    url(r'^user/(?P<pk>\d+)/cert-add/$', views.TesterCertAddView.as_view(), name="tester_cert_add"),
    url(r'^cert-edit/(?P<pk>\d+)/$', views.TesterCertEditView.as_view(), name="tester_cert_edit"),

    url(r'^user/(?P<pk>\d+)/kit-add/$', views.TestKitAddView.as_view(), name="test_kit_add"),
    url(r'^kit-edit/(?P<pk>\d+)/$', views.TestKitEditView.as_view(), name="test_kit_edit"),

    url(r'^test/(?P<pk>\d+)/pdf/$', views.SingleTestPDFView.as_view(), name="test_pdf"),
    url(r'^password/$', 'django.contrib.auth.views.password_change',
        {'post_change_redirect': '/password/edit/',
         'password_change_form': PasswordChangeWithMinLengthForm},
        name='password'),
    url(r'^audit-log/', AuditLogView.as_view(), name='audit_log'),

    url(r'^hazard/(?P<pk>\d+)/install-bp/$', views.BPDeviceCreateView.as_view(), name="bp_device_add"),
    url(r'^bp-device/(?P<pk>\d+)/edit/$', views.BPDeviceUpdateView.as_view(), name="bp_device_edit"),
    url(r'^bp-device/(?P<pk>\d+)/add-test/$', views.TestAddView.as_view(), name="test_add"),
    url(r'^registration', views.PwsOwnerRegistrationView.as_view(), name="pws_owner_registration"),
    url(r'^download-pdf', views.DownloadPublishedQuiz.as_view(), name="download_pdf"),
    url(r'^activate-blocked-pws', views.ActivateBlockedPWS.as_view(), name="activate_blocked_pws"),
    url(r'^demo-trial/pay/paypal/$', views.DemoTrialPayPaypalView.as_view(), name="demo_trial_paypal"),
    url(r'^test-price/$', views.TestPriceSetupView.as_view(), name='test_price')
)
