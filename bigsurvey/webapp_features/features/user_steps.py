from lettuce import step
from common_steps import click_link, click_element_by_xpath, check_text_exists, check_text_doesnt_exist, \
    check_multiple_text_exists
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


@step('I open "user_edit" page with pk "(\d+)" from tab (\d+)')
def open_user_edit_page(step, pk, tab):
    step.given('I open "user_list" page')
    click_element_by_xpath(Xpath.Pattern.user_page_tab % tab)
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


@step('Open user detail page with pk (\d+) from tab (\d+)')
def open_user_detail(step, pk, tab):
    open_user_list_page(step)
    click_element_by_xpath(Xpath.Pattern.user_page_tab % tab)
    click_link(step, "user_%s_detail" % pk)


@step('I directly open "tester_list" page')
def open_tester_list(step):
    step.given('I open "%s"' % get_url(Urls.tester_list))


@step('I should see following user in following tab')
def see_user_in_tab(step):
    for row in step.hashes:
        click_element_by_xpath(Xpath.Pattern.user_page_tab % row['tab'])
        check_text_exists(step, row['user'])


@step('I should not see following user in any of (\d+) tabs')
def not_see_user(step, tabs):
    for row in step.hashes:
        for i in range(1, int(tabs)+1):
            click_element_by_xpath(Xpath.Pattern.user_page_tab % i)
            check_text_doesnt_exist(step, row['user'])


@step('I should see following in tab (\d+)')
def see_multiple_text_in_user_tab(step, tab):
    click_element_by_xpath(Xpath.Pattern.user_page_tab % tab)
    check_multiple_text_exists(step)


@step('I should see "([ a-zA-Z0-9_-]+)" in tab (\d+)')
def see_text_in_user_tab(step, text, tab):
    click_element_by_xpath(Xpath.Pattern.user_page_tab % tab)
    check_text_exists(step, text)
