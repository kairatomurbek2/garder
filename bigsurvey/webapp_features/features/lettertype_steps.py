from django.core.urlresolvers import reverse
from common_steps import *
from lettuce import *
from data import *
from webapp import models
from webapp.models import PWS


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


@step('I directly open "letter_type_add" page')
def directly_open_letter_type_add_page(step):
    step.given('I open "%s"' % get_url(reverse('admin:webapp_lettertype_add')))


@step('I submit form with id "(.*)"')
def submit_letter_type_form(step, form_id):
    form_by_id = helper.find(Xpath.Pattern.form_by_id % form_id)
    helper.check_element_exists(form_by_id, 'Form with id "%s" was not found' % form_id)
    form_by_id.submit()


@step('Letter type with name "(.*)" was cloned to all PWS')
def check_new_letter_type(step, letter_type):
    for pws in PWS.objects.all():
        assert pws.letter_types.filter(letter_type=letter_type).exists(), 'PWS "%s" does not contain Letter Type "%s"' % (pws.name, letter_type)
