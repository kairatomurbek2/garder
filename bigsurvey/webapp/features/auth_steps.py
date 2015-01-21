from lettuce import *
from webapp.features.test_data import *


@step('Opened (.*) page')
def go_to_page(step, page):
    world.browser.get(get_url(UiElements.links[page]['url']))


@step('I login as (.*)')
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


@step('I (.*) - (.*) on page')
def see_or_not_on_page(step, reaction, text):
    if reaction == 'see':
        assert text in world.browser.page_source, '%s is not on page' % text
    else:
        assert text not in world.browser.page_source, '%s is on page' % text