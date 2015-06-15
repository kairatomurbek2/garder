from common_steps import *
from lettuce import *
from data import *
from webapp import models


@step('I directly open "letter_type_edit" page with pk "(\d+)"')
def directly_open_letter_type_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.letter_type_edit % pk))


@step('I open "letter_type_edit" page with pk "(\d+)"$')
def open_letter_type_edit_page(step, pk):
    step.given('I open "letter_type_list" page')
    step.given('I click "lettertype_%s_edit" link' % pk)

@step('I open "letter_type_list" page')
def open_letter_type_list_page(step):
    step.given('I open "home" page')
    step.given('I click "letter_type" menu link')


@step('I change template to "(.*)"')
def change_template_content(step, content):
    textarea = helper.find(Xpath.Pattern.textarea % 'template')
    textarea_id = textarea.get_attribute('id')
    iframe = world.browser.find_element_by_xpath('.//iframe[contains(@title, "%s")]' % textarea_id)
    world.browser.switch_to.frame(iframe)
    ckeditor = world.browser.find_element_by_tag_name('body')
    ckeditor.clear()
    ckeditor.send_keys(content)
    world.browser.switch_to.default_content()


@step('Letter type template with pk "(\d+)" should contain "(.*)"')
def check_letter_type_template_content(step, pk, content):
    letter_type = models.LetterType.objects.get(pk=pk)
    assert content in letter_type.template, '"%s" is not in "%s"' % (content, letter_type.template)
