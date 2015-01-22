from lettuce import *
from webapp.features.test_data import *

@step('I open (.*) page')
def go_to_page(step, page):
    world.browser.get(get_url(UiElements.links[page]['url']))


@step('I (.*) - (.*) on page')
def check_text_on_page(step, reaction, text):
    if reaction == 'see':
        assert text in world.browser.page_source, '%s is not on page' % text
    else:
        assert text not in world.browser.page_source, '%s is on page' % text


@step('I fill (.*) with (.*)')
def fill_field_with_value(step, field, value):
    field = world.browser.find_element_by_xpath(UiElements.Xpath.text_fields[field])
    field.clear()
    field.send_keys(value)


@step('I fill many (.*) with (.*)')
def fill_fields_with_values(step, fields, values):
    fields = fields.split(',')
    values = values.split(',')
    data = zip(fields, values)
    for pair in data:
        fill_field_with_value(step, pair[0], pair[1])


@step('I submit (.*) form')
def submit_form(step, form):
    world.browser.find_element_by_xpath(UiElements.Xpath.forms[form]).submit()