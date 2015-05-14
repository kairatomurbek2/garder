from common_steps import *
from lettuce import *
from data import *


@step('I directly open "pws_list" page')
def directly_open_pws_list_page(step):
    step.given('I open "%s"' % get_url(Urls.pws_list))


@step('I open "pws_list" page')
def open_pws_list_page(step):
    step.given('I open "home" page')
    step.given('I click "pws" menu link')


@step('I directly open "pws_add" page')
def directly_open_pws_add_page(step):
    step.given('I open "%s"' % get_url(Urls.pws_add))


@step('I open "pws_add" page')
def open_pws_add_page(step):
    step.given('I open "pws_list" page')
    step.given('I click "pws_add" link')


@step('I directly open "pws_edit" page with pk "(\d+)"')
def directly_open_pws_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.pws_edit % pk))


@step('I open "pws_edit" page with pk "(\d+)"')
def open_pws_edit_page(step, pk):
    step.given('I open "pws_list" page')
    step.given('I click "pws_%s_edit" link' % pk)


@step('I should be at "pws_list" page')
def check_pws_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.pws_list))


@step('I should be at "pws_add" page')
def check_pws_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.pws_add))


@step('I should be at "pws_edit" page with pk "(\d+)"')
def check_pws_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.pws_edit % pk))


@step('I should see "pws adding success" message')
def check_pws_adding_success_message(step):
    step.given('I should see "%s"' % Messages.PWS.adding_success)


@step('I should see "pws adding error" message')
def check_pws_adding_error_message(step):
    step.given('I should see "%s"' % Messages.PWS.adding_error)


@step('I should see "pws editing success" message')
def check_pws_editing_success_message(step):
    step.given('I should see "%s"' % Messages.PWS.editing_success)


@step('I should see "pws editing error" message')
def check_pws_editing_error_message(step):
    step.given('I should see "%s"' % Messages.PWS.editing_error)