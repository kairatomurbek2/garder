from common_steps import *
from lettuce import *
from data import *
from webapp.models import Test


@step('I directly open "test_add" page for hazard with pk "(\d+)"')
def open_test_add_page(step, hazard_pk):
    step.given('I open "%s"' % get_url(Urls.test_add % hazard_pk))


@step('I open "test_add" page for hazard with pk "(\d+)"')
def open_test_add_page(step, hazard_pk):
    step.given('I open "hazard_detail" page with pk "%s"' % hazard_pk)
    step.given('I click "hazard_%s_test_add" link' % hazard_pk)


@step('I directly open "test_edit" page with pk "(\d+)"')
def directly_open_test_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.test_edit % pk))


@step('I open "test_edit" page with pk "(\d+)"')
def open_test_edit_page(step, pk):
    hazard = Test.objects.get(pk=pk).bp_device
    step.given('I open "hazard_detail" page with pk "%s"' % hazard.pk)
    step.given('I click "test_%s_edit" link' % pk)


@step('I should be at "test_add" page for hazard with pk "(\d+)"')
def check_test_add_page(step, hazard_pk):
    step.given('I should be at "%s"' % get_url(Urls.test_add % hazard_pk))


@step('I should be at "test_edit" page with pk "(\d+)"')
def check_test_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.test_edit % pk))


@step('I should see "test adding success" message')
def check_test_adding_success_message(step):
    step.given('I should see "%s"' % Messages.Test.adding_success)


@step('I should see "test adding error" message')
def check_test_adding_error_message(step):
    step.given('I should see "%s"' % Messages.Test.adding_error)


@step('I should see "test editing success" message')
def check_test_editing_success_message(step):
    step.given('I should see "%s"' % Messages.Test.editing_success)


@step('I should see "test editing error" message')
def check_test_editing_error_message(step):
    step.given('I should see "%s"' % Messages.Test.editing_error)