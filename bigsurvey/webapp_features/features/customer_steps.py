from common_steps import *
from lettuce import *
from settings import *


@step('I directly open "customer_list" page')
def directly_open_customer_list_page(step):
    step.given('I open "%s"' % get_url(Urls.customer_list))


@step('I open "customer_list" page')
def open_customer_list_page(step):
    step.given('I open "home" page')
    step.given('I click "customers" menu link')


@step('I directly open "customer_detail" page with pk "(\d+)"')
def directly_open_customer_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.customer_detail % pk))


@step('I open "customer_detail" page with pk "(\d+)"')
def open_customer_detail_page(step, pk):
    step.given('I open "customer_list" page')
    step.given('I click "customer_%s_detail" link' % pk)


@step('I directly open "customer_add" page')
def directly_open_customer_add_page(step):
    step.given('I open "%s"' % get_url(Urls.customer_add))


@step('I open "customer_add" page')
def open_customer_add_page(step):
    step.given('I open "customer_list" page')
    step.given('I click "customer_add" link')


@step('I directly open "customer_edit" page with pk "(\d+)"')
def directly_open_customer_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.customer_edit % pk))


@step('I open "customer_edit" page with pk "(\d+)"')
def open_customer_edit_page(step, pk):
    step.given('I open "customer_list" page')
    step.given('I click "customer_%s_edit" link' % pk)


@step('I should be at "customer_list" page')
def check_customer_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.customer_list))


@step('I should be at "customer_add" page')
def check_customer_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.customer_add))


@step('I should be at "customer_edit" page with pk "(\d+)"')
def check_customer_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.customer_edit % pk))


@step('I should see "customer adding success" message')
def check_customer_adding_success_message(step):
    step.given('I should see "%s"' % Messages.Customer.adding_success)


@step('I should see "customer adding error" message')
def check_customer_adding_error_message(step):
    step.given('I should see "%s"' % Messages.Customer.adding_error)


@step('I should see "customer editing success" message')
def check_customer_editing_success_message(step):
    step.given('I should see "%s"' % Messages.Customer.editing_success)


@step('I should see "customer editing error" message')
def check_customer_editing_error_message(step):
    step.given('I should see "%s"' % Messages.Customer.editing_error)