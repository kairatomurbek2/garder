import helper
from lettuce import *
from settings import *


@step(r'I open "(http.*)"')
def open_url(step, url):
    world.browser.get(url)


@step('I should be at "(http.*)"')
def check_url(step, url):
    assert world.browser.current_url == url, "Current URL is %s, expected %s" % (world.browser.current_url, url)


@step('I should see "([^"]*)"$')
def check_text_exists(step, text):
    helper.check_text_exists(text, '"%s" is not on page.' % text)


@step('I should not see "([^"]*)"$')
def check_text_doesnt_exist(step, text):
    helper.check_text_doesnt_exist(text, '"%s" in on page.' % text)


@step('I should see following$')
def check_multiple_text_exists(step):
    for row in step.hashes:
        step.given('I should see "%s"' % row['text'])


@step('I should not see following$')
def check_multiple_text_doesnt_exist(step):
    for row in step.hashes:
        step.given('I should not see "%s"' % row['text'])


@step('I fill in "([-_a-z0-9]+)" with "(.*)"')
def fill_in_textfield(step, field_name, value):
    field = helper.find(Xpath.Pattern.input % field_name) or \
            helper.find(Xpath.Pattern.textarea % field_name)
    helper.check_element_exists(field, 'Field "%s" was not found' % field_name)
    field.clear()
    field.send_keys(value)


@step('I fill in following fields with following values')
def fill_in_multiple_textfields(step):
    for row in step.hashes:
        step.given('I fill in "%s" with "%s"' % (row['field'], row['value']))


@step('I select "(.*)" from "([-_a-z0-9]+)"')
def select_option(step, value, select_name):
    select = helper.find(Xpath.Pattern.select % select_name)
    helper.check_element_exists(select, 'Select "%s" was not found' % select_name)
    option = helper.find(Xpath.Pattern.option_by_value % value, context=select) or \
             helper.find(Xpath.Pattern.option_by_exact_text % value, context=select) or \
             helper.find(Xpath.Pattern.option_by_substr % value, context=select)
    assert option, 'Option with value "%s" was not found' % value
    option.click()


@step('I submit "([-_a-z0-9]+)" form')
def submit_form(step, form_name):
    form = helper.find(Xpath.Pattern.form % form_name)
    helper.check_element_exists(form, 'Form "%s" was not found' % form_name)
    form.submit()


@step('I should see "(.*)" validation error message on field "([-_a-z0-9]+)"')
def check_error_message(step, error_message, field_name):
    field = helper.find(Xpath.Pattern.input % field_name) or \
            helper.find(Xpath.Pattern.textarea % field_name) or \
            helper.find(Xpath.Pattern.select % field_name)
    helper.check_element_exists(field, 'Field "%s" was not found' % field_name)
    error = helper.find(Xpath.Pattern.validation_error_by_exact_text % error_message, field) or \
            helper.find(Xpath.Pattern.validation_error_by_substr % error_message, field)
    helper.check_element_exists(error, 'Field "%s" does not contain "%s" validation error message' % (field_name, error_message))


@step('I should see following validation error messages on following fields')
def check_multiple_error_messages(step):
    for row in step.hashes:
        step.given('I should see "%s" validation error message on field "%s"' % (row['error_message'], row['field']))