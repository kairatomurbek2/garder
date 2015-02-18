from common_steps import *
from lettuce import *
from settings import *


@step('I directly open "inspection_list" page')
def directly_open_inspection_list_page(step):
    step.given('I open "%s"' % get_url(Urls.inspection_list))


@step('I open "inspection_list" page')
def open_inspection_list_page(step):
    step.given('I open "home" page')
    step.given('I click "inspections" menu link')


@step('I directly open "inspection_add" page for site with pk "(\d+)"')
def directly_open_inspection_add_page(step, site_pk):
    step.given('I open "%s"' % get_url(Urls.inspection_add % site_pk))


@step('I open "inspection_add" page for site with pk "(\d+)"')
def open_inspection_add_page(step, site_pk):
    step.given('I open "site_detail" page with pk "%s"' % site_pk)
    step.given('I hover on "assign" link')
    step.given('I click "site_%s_inspection_add" link' % site_pk)


@step('I directly open "inspection_edit" page with pk "(\d+)"')
def directly_open_inspection_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.inspection_edit % pk))


@step('I open "inspection_edit" page with pk "(\d+)"')
def open_inspection_edit_page(step, pk):
    step.given('I open "inspection_list" page')
    step.given('I click "inspection_%s_edit" link' % pk)


@step('I should be at "inspection_list" page')
def check_inspection_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.inspection_list))


@step('I should be at "inspection_add" page for site with pk "(\d+)"')
def check_inspection_add_page(step, site_pk):
    step.given('I should be at "%s"' % get_url(Urls.inspection_add % site_pk))


@step('I should be at "inspection_edit" page with pk "(\d+)"')
def check_inspection_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.inspection_edit % pk))


@step('I should see "inspection adding success" message')
def check_inspection_adding_success_message(step):
    step.given('I should see "%s"' % Messages.Inspection.adding_success)


@step('I should see "inspection adding error" message')
def check_inspection_adding_error_message(step):
    step.given('I should see "%s"' % Messages.Inspection.adding_error)


@step('I should see "inspection editing success" message')
def check_inspection_editing_success_message(step):
    step.given('I should see "%s"' % Messages.Inspection.editing_success)


@step('I should see "inspection editing error" message')
def check_inspection_editing_error_message(step):
    step.given('I should see "%s"' % Messages.Inspection.editing_error)