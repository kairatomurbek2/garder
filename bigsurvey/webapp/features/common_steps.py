from lettuce import *
from settings import *
from selenium.common.exceptions import *


@step('I go to "([a-z0-9_]+)" page$')
@step('I visit "([a-z0-9_]+)" page$')
@step('I open "([a-z0-9_]+)" page$')
def open_page(step, page):
    world.browser.get(get_url(URLS[page]))


@step('I go to "([a-z0-9_]+)" page with params "(.*)"')
@step('I visit "([a-z0-9_]+)" page with params "(.*)"')
@step('I open "([a-z0-9_]+)" page with params "(.*)"')
def open_page_with_params(step, page, params):
    params = params.split(' :: ')
    world.browser.get(get_url(URLS[page] % tuple(params)))


@step(r'I go to "(http.*)"')
@step(r'I visit "(http.*)"')
@step(r'I open "(http.*)"')
def open_url(step, url):
    world.browser.get(url)


@step('I should (see|not see) "(.*)"')
def check_content(step, reaction, text):
    if reaction == 'see':
        assert text in world.browser.page_source, '%s is not on page' % text
    else:
        assert text not in world.browser.page_source, '%s is on page' % text


@step('I should be at "(.*)" page')
def check_page(step, page):
    assert world.browser.current_url == get_url(URLS[page]), "Current URL is %s, expected %s" % (
        world.browser.current_url, get_url(URLS[page]))


@step('I should be at "([a-z0-9_]+)" page with params "(.*)"')
def check_page_with_params(step, page, params):
    params = params.split(' :: ')
    assert world.browser.current_url == get_url(URLS[page] % tuple(params)), "Current URL is %s, expected %s" % (
        world.browser.current_url, get_url(URLS[page] % tuple(params)))


@step('I should be at "(http.*)"')
def check_url(step, url):
    assert world.browser.current_url == url, "Current URL is %s, expected %s" % (world.browser.current_url, url)


@step('I click on "([a-z0-9_]+)" link')
def click_on_link(step, link):
    link = world.browser.find_element_by_xpath(Xpath.links[link])
    link.click()


@step('I press "([a-z0-9_]+)" button')
def press_button(step, button):
    button = world.browser.find_element_by_xpath(Xpath.buttons[button])
    button.click()


@step('I fill in "([a-z0-9_]+)" with "(.*)"')
def fill_in_textfield(step, field, value):
    field = world.browser.find_element_by_xpath(Xpath.text_fields[field])
    field.clear()
    field.send_keys(value)


@step('I fill in the following "([a-z0-9_: ]+)" with following "(.*)"')
def fill_in_multiple_textfields(step, fields, values):
    fields = fields.split(' :: ')
    values = values.split(' :: ')
    assert len(fields) == len(values), "Fields and values should contains the same number of elements"
    data = zip(fields, values)
    for pair in data:
        step.given('I fill in "%s" with "%s"' % (pair[0], pair[1]))


@step('I submit "([a-z0-9_]+)" form')
def submit_form(step, form):
    form = world.browser.find_element_by_xpath(Xpath.forms[form])
    form.submit()


@step('I select "(.*)" from "([a-z0-9_]+)"')
def select_option(step, value, select):
    select = world.browser.find_element_by_xpath(Xpath.selects[select])
    try:
        option = select.find_element_by_xpath(str('.//option[@value="%s"]' % value))
    except NoSuchElementException:
        option = select.find_element_by_xpath(str('.//option[contains(., "%s")]' % value))
    option.click()