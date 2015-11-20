from lettuce import step
import common_steps
import user_steps
from data import Urls, get_url
from webapp.models import TestKit, TesterCert


@step('I directly open "kit_add" page with pk (\d+)')
def dir_open_kit_add_page(step, pk):
    common_steps.open_url(step, get_url(Urls.kit_add % pk))


@step('I directly open "kit_edit" page with pk (\d+)')
def dir_open_kit_edit_page(step, pk):
    common_steps.open_url(step, get_url(Urls.kit_edit % pk))


@step('I directly open "cert_add" page with pk (\d+)')
def dir_open_cert_add_page(step, pk):
    common_steps.open_url(step, get_url(Urls.cert_add % pk))


@step('I directly open "cert_edit" page with pk (\d+)')
def dir_open_cert_edit_page(step, pk):
    common_steps.open_url(step, get_url(Urls.cert_edit % pk))


@step('I open "kit_add" page with pk (\d+)')
def open_kit_add_page(step, pk):
    user_steps.open_user_detail(step, pk, 5)
    common_steps.click_link(step, "kit_add")


@step('I open "kit_edit" page with pk (\d+)')
def open_kit_edit_page(step, pk):
    kit = TestKit.objects.get(pk=pk)
    user_steps.open_user_detail(step, kit.user.pk, 5)
    common_steps.click_link(step, "kit_%s_edit" % pk)


@step('I open "cert_add" page with pk (\d+)')
def open_cert_add_page(step, pk):
    user_steps.open_user_detail(step, pk, 5)
    common_steps.click_link(step, "cert_add")


@step('I open "cert_edit" page with pk (\d+)')
def open_cert_edit_page(step, pk):
    cert = TesterCert.objects.get(pk=pk)
    user_steps.open_user_detail(step, cert.user.pk, 5)
    common_steps.click_link(step, "cert_%s_edit" % pk)


@step('I should be at "user_detail" page with pk (\d+)')
def is_at_user_detail(step, pk):
    common_steps.check_url(step, get_url(Urls.user_detail % pk))
