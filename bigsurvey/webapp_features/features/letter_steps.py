from common_steps import *
from lettuce import *
from settings import *
from webapp.models import Letter

WARNING_LETTER_MESSAGE = "Warning: {AssemblyType} has no value in database"
WARNING_DUE_DATE_MESSAGE = "Warning: {DueDate} has no value in database"


@step('I open "letter_list" page')
def open_letter_list_page(step):
    step.given('I click "letters_menu" link')


@step('I directly open "letter_list" page')
def directly_open_letter_list_page(step):
    step.given('I open "%s"' % get_url(Urls.letter_list))


@step('I directly open "letter_detail" page with pk "(\d+)"')
def directly_open_letter_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.letter_detail % pk))


@step('I open "letter_detail" page with pk "(\d+)"')
def open_letter_detail_page(step, pk):
    step.given('I open "letter_list" page')
    step.given('I click "letter_%s_detail" link' % pk)


@step('I directly open "letter_add" page for site with pk "(\d+)"')
def directly_open_letter_add_page_for_site(step, site_pk):
    step.given('I open "%s"' % get_url(Urls.letter_add % site_pk))


@step('I open "letter_add" page for site with pk "(\d+)"')
def open_letter_add_page_for_site(step, site_pk):
    step.given('I open "site_detail" page with pk "%s"' % site_pk)
    step.given('I click "site_%s_letter" link' % site_pk)


@step('I should be at "letter_detail" page with pk "(\d+)"')
def check_letter_detail_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.letter_detail % pk))


@step('I should be at "letter_add" page for site with pk "(\d+)"')
def check_letter_add_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.letter_add % pk))


@step('I should see "letter adding success" message')
def see_letter_adding_success(step):
    step.given('I should see "%s"' % Messages.Letter.adding_success)


@step('I should see warning letter message')
def see_warning_letter_message(step):
    step.then('I should see "%s"' % WARNING_LETTER_MESSAGE)


@step('letter is deleted')
def delete_fresh_added_letter(step):
    Letter.objects.filter(letter_type__letter_type="Pool").delete()


@step('I should see "letter adding error" message')
def see_letter_adding_error_message(step):
    step.then('I should see "%s"' % Messages.Letter.adding_error)


@step('I directly open "letter_edit" page with pk "(\d+)"')
def directly_open_hazard_add_page_for_site(step, pk):
    step.given('I open "%s"' % get_url(Urls.letter_edit % pk))


@step('I open "letter_edit" page with pk "(\d+)"$')
def open_hazard_edit_page(step, pk):
    step.given('I open "letter_detail" page with pk "%s"' % pk)
    step.given('I click "letter_%s_edit" link' % pk)
    

@step('I should see "letter editing success" message')
def see_letter_editing_success(step):
    step.given('I should see "%s"' % Messages.Letter.editing_success)


@step('I should see warning due date letter message')
def see_warning_letter_message(step):
    step.then('I should see "%s"' % WARNING_DUE_DATE_MESSAGE)
    

@step('I should see "letter editing error" message')
def see_letter_editing_error_message(step):
    step.then('I should see "%s"' % Messages.Letter.editing_error)
    

@step('I should be at "letter_edit" page for site with pk "(\d+)"')
def check_letter_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.letter_edit % pk))