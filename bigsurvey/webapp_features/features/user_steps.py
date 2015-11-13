from lettuce import step
from common_steps import click_link

from data import *
from main.parameters import Messages


@step('I directly open "user_list" page')
def directly_open_user_list_page(step):
    step.given('I open "%s"' % get_url(Urls.user_list))


@step('I open "user_list" page')
def open_user_list_page(step):
    step.given('I open "home" page')
    step.given('I click "users" menu link')


@step('I directly open "user_add" page')
def directly_open_user_add_page(step):
    step.given('I open "%s"' % get_url(Urls.user_add))


@step('I open "user_add" page')
def open_user_add_page(step):
    step.given('I open "user_list" page')
    step.given('I click "user_add" link')


@step('I directly open "user_edit" page with pk "(\d+)"')
def directly_open_user_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.user_edit % pk))


@step('I open "user_edit" page with pk "(\d+)"')
def open_user_edit_page(step, pk):
    step.given('I open "user_list" page')
    step.given('I click "user_%s_edit" link' % pk)


@step('I should be at "user_list" page')
def check_user_list_page(step):
    step.given('I should be at "%s"' % get_url(Urls.user_list))


@step('I should be at "user_add" page')
def check_user_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.user_add))


@step('I should be at "user_edit" page with pk "(\d+)"')
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


@step('Open user detail page with pk (\d+)')
def open_user_detail(step, pk):
    open_user_list_page(step)
    click_link(step, "user_%s_detail" % pk)
