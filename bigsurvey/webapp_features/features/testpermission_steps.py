from common_steps import *
from lettuce import *
from settings import *


@step('I directly open "testpermission_list" page')
def directly_open_testpermission_list_page(step):
    step.given('I open "%s"' % get_url(Urls.testpermission_list))


@step('I open "testpermission_list" page')
def open_testpermission_list_page(step):
    step.given('I open "home" page')
    step.given('I click "testpermissions" menu link')


@step('I directly open "testpermission_add" page for site with pk "(\d+)"')
def directly_open_testpermission_add_page(step, site_pk):
    step.given('I open "%s"' % get_url(Urls.testpermission_add % site_pk))


@step('I open "testpermission_add" page for site with pk "(\d+)"')
def open_testpermission_add_page(step, site_pk):
    step.given('I open "site_detail" page with pk "%s"' % site_pk)
    step.given('I hover on "assign" link')
    step.given('I click "site_%s_testpermission_add" link' % site_pk)


@step('I open "testpermission_edit" page with pk "(\d+)"')
def open_testpermission_edit_page(step, pk):
    step.given('I open "testpermission_list" page')
    step.given('I click "testpermission_%s_edit" link' % pk)


@step('I directly open "testpermission_edit" page with pk "(\d+)"')
def directly_open_testpermission_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.testpermission_edit % pk))


@step('I should be at "testpermission_list" page')
def check_testpermission_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.testpermission_list))


@step('I should be at "testpermission_add" page for site with pk "(\d+)"')
def check_testpermission_add_page(step, site_pk):
    step.given('I should be at "%s"' % get_url(Urls.testpermission_add % site_pk))


@step('I should be at "testpermission_edit" page with pk "(\d+)"')
def check_testpermission_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.testpermission_edit % pk))


@step('I should see "testpermission adding success" message')
def check_testpermission_adding_success_message(step):
    step.given('I should see "%s"' % Messages.TestPermission.adding_success)


@step('I should see "testpermission adding error" message')
def check_testpermission_adding_error_message(step):
    step.given('I should see "%s"' % Messages.TestPermission.adding_error)


@step('I should see "testpermission editing success" message')
def check_testpermission_editing_success_message(step):
    step.given('I should see "%s"' % Messages.TestPermission.editing_success)


@step('I should see "testpermission editing error" message')
def check_testpermission_editing_error_message(step):
    step.given('I should see "%s"' % Messages.TestPermission.editing_error)