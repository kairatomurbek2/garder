from common_steps import *
from lettuce import *
from settings import *


@step('I open "user list" page')
def open_user_list_page(step):
    step.given('I open "%s"' % get_url(Urls.user_list))


@step('I open "user add" page')
def open_user_add_page(step):
    step.given('I open "%s"' % get_url(Urls.user_add))


@step('I open "user edit" page with pk "(\d+)"')
def open_user_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.user_edit % pk))


@step('I should be at "user list" page')
def check_user_list_page(step):
    step.given('I should be at "%s"' % get_url(Urls.user_list))


@step('I should be at "user add" page')
def check_user_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.user_add))


@step('I should be at "user edit" page with pk "(\d+)"')
def check_user_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.user_edit % pk))


@step('I should see "user adding success" message')
def check_user_adding_success_message(step):
    step.given('I should see "%s"' % Messages.User.adding_success)


@step('I should see "user adding error" message')
def check_user_adding_error_message(step):
    step.given('I should see "%s"' % Messages.User.adding_error)


@step('I should see "user editing success" message')
def check_user_editing_success_message(step):
    step.given('I should see "%s"' % Messages.User.editing_success)


@step('I should see "user editing error" message')
def check_user_editing_error_message(step):
    step.given('I should see "%s"' % Messages.User.editing_error)