import time

import datetime

import helper
import os
from django.conf import settings
from lettuce import step, world
from webapp_features.features.data import Urls
from webapp_features.features.data import get_url, Xpath


@step('I open "(http.*)"')
def open_url(step, url):
    world.browser.get(url)


@step('I open "home" page')
def open_home_page(step):
    step.given('I open "%s"' % get_url(Urls.home))


@step('I click "(.*)" link$')
def click_link(step, link_name):
    link = helper.find(Xpath.Pattern.link % link_name) or \
           helper.find(Xpath.Pattern.link_by_href % link_name) or \
           helper.find(Xpath.Pattern.link_by_exact_text % link_name) or \
           helper.find(Xpath.Pattern.link_by_substr % link_name)
    helper.check_element_exists(link, 'Link with name "%s" was not found' % link_name)
    link.click()


@step('click url')
def click_url(step):
    elements = helper.find(Xpath.Pattern.link_a)
    import time; time.sleep(6)
    elements.click()


@step('I should be at "(http.*)"')
def check_url(step, url):
    assert world.browser.current_url == url, 'Current URL is %s, expected %s' % (world.browser.current_url, url)


@step('I should see "([^"]*)"$')
def check_text_exists(step, text):
    helper.check_text_exists(text, '"%s" is not on page.' % text)


@step('I should not see "([^"]*)"$')
def check_text_doesnt_exist(step, text):
    helper.check_text_doesnt_exist(text, '"%s" is on page.' % text)


@step('I should see following$')
def check_multiple_text_exists(step):
    for row in step.hashes:
        step.given('I should see "%s"' % row['text'])


@step('I should not see following$')
def check_multiple_text_doesnt_exist(step):
    for row in step.hashes:
        step.given('I should not see "%s"' % row['text'])


@step('I choose today in "([-_a-z0-9]+)"')
def choose_today(step, field_name):
    today = datetime.datetime.today()
    today_as_string = today.strftime('%Y-%m-%d')
    step.given('I fill in "%s" with "%s"' % (field_name, today_as_string))


@step('I fill in "([-_a-z0-9]+)" with "(.*)"')
def fill_in_textfield(step, field_name, value):
    field = helper.find(Xpath.Pattern.input % field_name) or \
            helper.find(Xpath.Pattern.textarea % field_name)
    helper.check_element_exists(field, 'Field "%s" was not found' % field_name)
    field.clear()
    field.send_keys(value)


@step('I fill in file input "([-_a-z0-9]+)" with "(.*)"')
def fill_in_file_field(step, field_name, filename):
    field = helper.find(Xpath.Pattern.file_input % field_name)
    helper.check_element_exists(field, 'File field "%s" was not found' % field_name)
    full_filepath = os.path.join(settings.STUB_FILES_DIR, filename)
    field.send_keys(full_filepath)


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
    helper.check_element_exists(option, 'Option with value "%s" was not found' % value)
    option.click()


@step('I submit "([-_a-z0-9]+)" form')
def submit_form(step, form_name):
    form = helper.find(Xpath.Pattern.form % form_name)
    helper.check_element_exists(form, 'Form "%s" was not found' % form_name)
    form.submit()


@step('I submit survey form$')
def submit_survey_form(step):
    submit_btn = helper.find(Xpath.Pattern.survey_form_submit_btn)
    submit_btn.click()


@step('I submit hazard adding form')
def submit_hazard_adding_form(step):
    submit_btn = helper.find(Xpath.Pattern.hazard_addition_submit_btn)
    submit_btn.click()


@step('I one submit hazard adding form')
def submit_hazard_adding_form_one(step):
    submit_btn = helper.find(Xpath.Pattern.hazard_addition_submit_btn_one)
    submit_btn.click()


@step('I two submit hazard adding form')
def submit_hazard_adding_form_two(step):
    submit_btn = helper.find(Xpath.Pattern.hazard_addition_submit_btn_two)
    submit_btn.click()


@step('I three submit hazard adding form')
def submit_hazard_adding_form_three(step):
    submit_btn = helper.find(Xpath.Pattern.hazard_addition_submit_btn_three)
    submit_btn.click()


@step('I should see "(.*)" validation error message on field "([-_a-z0-9]+)"')
def check_error_message(step, error_message, field_name):
    field = helper.find(Xpath.Pattern.input % field_name) or \
            helper.find(Xpath.Pattern.textarea % field_name) or \
            helper.find(Xpath.Pattern.select % field_name)
    helper.check_element_exists(field, 'Field "%s" was not found' % field_name)
    error = helper.find(Xpath.Pattern.validation_error_by_exact_text % error_message, field) or \
            helper.find(Xpath.Pattern.validation_error_by_substr % error_message, field) or \
            helper.find(Xpath.Pattern.custom_validation_error_on_survey_form % error_message)
    helper.check_element_exists(error, 'Field "%s" does not contain "%s" validation error message' % (field_name, error_message))


@step('I should see following validation error messages on following fields')
def check_multiple_error_messages(step):
    for row in step.hashes:
        step.given('I should see "%s" validation error message on field "%s"' % (row['error_message'], row['field']))


@step('I click "([-_a-z0-9]+)" button')
def click_button(step, button_name):
    button = helper.find(Xpath.Pattern.button % button_name)
    helper.check_element_exists(button, 'Button with name "%s" was not found' % button_name)
    button.click()


@step('I click button with label "([-_a-zA-Z0-9 ]+)"')
def click_button_with_label(step, label):
    button = helper.find(Xpath.Pattern.button_with_label % label)
    helper.check_element_exists(button, 'Button with label "%s" was not found' % label)
    button.click()


@step('I should see "(.*)" option in "(.*)" select')
def check_option_in_select_exists(step, option_value, select_name):
    select = helper.find(Xpath.Pattern.select % select_name)
    helper.check_element_exists(select, 'Select "%s" was not found' % select_name)
    option = helper.find(Xpath.Pattern.option_by_value % option_value, context=select) or \
             helper.find(Xpath.Pattern.option_by_exact_text % option_value, context=select) or \
             helper.find(Xpath.Pattern.option_by_substr % option_value, context=select)
    helper.check_element_exists(option, 'Option with value "%s" was not found' % option_value)


@step('I should not see "(.*)" option in "(.*)" select')
def check_option_in_select_doesnt_exist(step, option_value, select_name):
    select = helper.find(Xpath.Pattern.select % select_name)
    helper.check_element_exists(select, 'Select "%s" was not found' % select_name)
    option = helper.find(Xpath.Pattern.option_by_value % option_value, context=select) or \
             helper.find(Xpath.Pattern.option_by_exact_text % option_value, context=select) or \
             helper.find(Xpath.Pattern.option_by_substr % option_value, context=select)
    helper.check_element_doesnt_exist(option, 'Option with value "%s" was found' % option_value)


@step('I should see following options in following selects')
def check_multiple_options_in_select_exist(step):
    for pair in step.hashes:
        step.given('I should see "%s" option in "%s" select' % (pair['option'], pair['select']))


@step('I should not see following options in following selects')
def check_multiple_options_in_select_doesnt_exist(step):
    for pair in step.hashes:
        step.given('I should not see "%s" option in "%s" select' % (pair['option'], pair['select']))


@step('I choose "(.*)" from "([-_a-z0-9]+)"')
def choose_value_from_radiobutton(step, value, radiobutton_name):
    radiobutton = helper.find(Xpath.Pattern.radiobutton_by_value % (radiobutton_name, value))
    helper.check_element_exists(radiobutton, 'Radiobutton "%s" with value "%s" was not found' % (radiobutton_name, value))
    radiobutton.click()


@step('I check "(.*)" from "([-_a-z0-9]+)"')
def check_value_from_checkbox(step, value, checkbox_name):
    checkbox = helper.find(Xpath.Pattern.checkbox_by_value % (checkbox_name, value))
    helper.check_element_exists(checkbox, 'Checkbox "%s" with value "%s" was not found' % (checkbox_name, value))
    checkbox.click()


@step('I check hazard "([^"]*)"$')
def check_hazard(step, hazard_name):
    checkbox = helper.find(Xpath.Pattern.survey_hazard % hazard_name)
    helper.check_element_exists(checkbox, 'Checkbox with text "%s" was not found' % (hazard_name))
    checkbox.click()


@step('I check "([-_a-z0-9]+)"$')
def check_single_checkbox(step, checkbox_name):
    checkbox = helper.find(Xpath.Pattern.checkbox_by_name % checkbox_name)
    helper.check_element_exists(checkbox, 'Checkbox "%s" was not found' % checkbox_name)
    checkbox.click()


@step('I uncheck "([-_a-z0-9]+)"$')
def check_single_checkbox(step, checkbox_id):
    checkbox = helper.find(Xpath.Pattern.checkbox_by_id % checkbox_id)
    helper.check_element_exists(checkbox, 'Checkbox "%s" was not found' % checkbox_id)
    checkbox.click()


@step('I check following values from "([-_a-z0-9]+)"')
def check_multiple_values_from_checkbox(step, checkbox_name):
    for row in step.hashes:
        step.given('I check "%s" from "%s"' % (row['value'], checkbox_name))


@step('I wait for (\d+) seconds?')
def wait_seconds(step, seconds):
    time.sleep(float(seconds))


@step('I refresh page')
def refresh_page(step):
    world.browser.refresh()


def click_element_by_xpath(xpath):
    element = helper.find(xpath)
    element.click()


@step('Sleep (\d+)')
def sleep_step(step, seconds):
    # to debug f***ing tests
    time.sleep(float(seconds))


@step('I should see text "(.+)" (\d+) times')
def see_text_n_times(step, text, n):
    elements = helper.find_multiple(Xpath.Pattern.element_with_text % text)
    m = len(elements)
    assert(m == n, "Expected %s items, found %s." % (n, m))
