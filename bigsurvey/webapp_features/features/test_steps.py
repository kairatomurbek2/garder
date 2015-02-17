from common_steps import *
from lettuce import *
from settings import *


@step('I open "test add" page for hazard with pk "(\d+)"')
def open_test_add_page(step, hazard_pk):
    step.given('I open "%s"' % get_url(Urls.test_add % hazard_pk))


@step('I open "test edit" page with pk "(\d+)"')
def open_test_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.test_edit % pk))


@step('I should be at "test add" page for hazard with pk "(\d+)"')
def check_test_add_page(step, hazard_pk):
    step.given('I should be at "%s"' % get_url(Urls.test_add % hazard_pk))


@step('I should be at "test edit" page with pk "(\d+)"')
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