from lettuce import *
from webapp.features.test_data import *


@step('I go to (.*) page')
def go_to_page(step, page):
    world.browser.get(get_url(UiElements.links[page]['url']))


@step('Login as (.*)')
def login_as(step, role):
    requisites = TestData.logins[role]
    login(step, requisites['username'], requisites['password'])


@step('Login with username (.*) and password (.*)')
def login(step, username, password):
    username_field = world.browser.find_element_by_xpath(UiElements.Xpath.text_fields['auth_username'])
    username_field.send_keys(username)
    password_field = world.browser.find_element_by_xpath(UiElements.Xpath.text_fields['auth_password'])
    password_field.send_keys(password)
    world.browser.find_element_by_xpath(UiElements.Xpath.buttons['auth_submit']).submit()


@step('I see (.*) on page')
def see_on_page(step, text):
    assert text in world.browser.page_source, '%s is not on page' % text


@step('I do not see (.*) on page')
def do_not_see_on_page(step, text):
    assert text not in world.browser.page_source, '% is on page' % text