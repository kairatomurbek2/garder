from helper import *
from lettuce import *
from settings import *


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


@step('I should (see|not see) following "(.*)"')
def check_multiple_content(step, reaction, text):
    text = text.split(' :: ')
    for item in text:
        step.given('I should %s "%s"' % (reaction, item))


@step('I should (see|not see) element with ([-a-z]+)="([-_a-z0-9]+)"')
def check_elem_by_attr(step, reaction, attr, value):
    elem = find_elem_by_xpath('//*[@%s="%s"]' % (attr, value))
    if reaction == 'see':
        assert elem, 'Element with %s="%s" was not found' % (attr, value)
    else:
        assert not elem, 'Element with %s="%s" was found' % (attr, value)


@step('I should (see|not see) elements with ([-a-z]+)="([-_a-z0-9: ]+)"')
def check_multiple_elem_by_attr(step, reaction, attr, values):
    values = values.split(' :: ')
    for item in values:
        step.given('I should %s element with %s="%s"' % (reaction, attr, item))


@step('I should be at "(.*)" page$')
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
def click_on_link(step, link_name):
    link = find_elem_by_xpath(Xpath.links[link_name])
    assert link, 'Link "%s" was not found' % link_name
    link.click()


@step('I press "([a-z0-9_]+)" button')
def press_button(step, button_name):
    button = find_elem_by_xpath(Xpath.buttons[button_name])
    assert button, 'Button "%s" was not found' % button_name
    button.click()


@step('I fill in "([a-z0-9_]+)" with "(.*)"')
def fill_in_textfield(step, field_name, value):
    field = find_elem_by_xpath(Xpath.text_fields[field_name])
    assert field, 'Field "%s" was not found' % field_name
    field.clear()
    field.send_keys(value)


@step('I fill in following fields "([a-z0-9_: ]+)" with following values "(.*)"')
def fill_in_multiple_textfields(step, fields, values):
    fields = fields.split(' :: ')
    values = values.split(' :: ')
    assert len(fields) == len(values), "Fields and values should contains the same number of elements"
    data = zip(fields, values)
    for pair in data:
        step.given('I fill in "%s" with "%s"' % (pair[0], pair[1]))


@step('I submit "([a-z0-9_]+)" form')
def submit_form(step, form_name):
    form = find_elem_by_xpath(Xpath.forms[form_name])
    assert form, 'Form "%s" was not found' % form_name
    form.submit()


@step('I select "(.*)" from "([a-z0-9_]+)"')
def select_option(step, value, select_name):
    select = find_elem_by_xpath(Xpath.selects[select_name])
    assert select, 'Select "%s" was not found' % select_name
    option = find_elem_by_xpath(str('.//option[@value="%s"]' % value), context=select) or \
             find_elem_by_xpath(str('.//option[. = "%s"]' % value), context=select)
    assert option, 'Option with value "%s" was not found' % value
    option.click()