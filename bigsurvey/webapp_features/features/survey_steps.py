from common_steps import *
from lettuce import *
from data import *
from webapp.models import Survey


@step('I click survey detail link with number "(.*)"')
def click_survey_detail_link(step, number):
    link = helper.find(Xpath.Pattern.survey_detail % number)
    helper.check_element_exists(link, 'Link with number "%s" was not found' % number)
    link.click()


@step('I click survey edit link')
def click_survey_detail_link(step):
    link = helper.find(Xpath.Pattern.survey_edit_link)
    helper.check_element_exists(link, 'Survey edit link was not found')
    link.click()


@step('I directly open "survey_detail" page with pk "(\d+)"')
def directly_open_survey_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.survey_detail % pk))


@step('I open "survey_detail" page with pk "(\d+)"')
def open_survey_detail_page(step, pk):
    site = Survey.objects.get(pk=pk).site
    step.given('I open "site_detail" page with pk "%s"' % site.pk)
    step.given('I click "survey_%s_detail" link' % pk)


@step('I directly open "survey_add" page for site with pk "(\d+)" and service "([a-z]+)"')
def directly_open_survey_add_page_for_site(step, site_pk, service_type):
    step.given('I open "%s"' % get_url(Urls.survey_add % (site_pk, service_type)))


@step('I open "survey_add" page for site with pk "(\d+)" and service "([a-z]+)"')
def open_survey_add_page_for_site(step, site_pk, service_type):
    step.given('I open "site_detail" page with pk "%s"' % site_pk)
    click_element_by_xpath(Xpath.Pattern.site_surveys_button)
    step.given('I click "s%s" link' % service_type)
    step.given('I click "site_%s_service_%s_survey_add" link' % (site_pk, service_type))


@step('I directly open "survey_edit" page with pk "(\d+)"')
def directly_open_survey_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.survey_edit % pk))


@step('I open "survey_edit" page with pk "(\d+)"')
def open_survey_edit_page(step, pk):
    step.given('I open "survey_detail" page with pk "%s"' % pk)
    step.given('I click "survey_%s_edit" link' % pk)


@step('I click "(\d+)"th "survey_detail" link on page')
def click_survey_detail_link(step, number):
    step.given('I click survey detail link with number "%s"' % number)


@step('I open "survey_edit" page for survey no "(\d+)" on the page')
def open_survey_edit_page(step, pk):
    step.given('I click "%s"th "survey_detail" link on page' % pk)
    step.given('I click survey edit link')


@step('I should be at "survey_detail" page with pk "(\d+)"')
def check_survey_detail_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.survey_detail % pk))


@step('I should be at "survey_add" page for site with pk "(\d+)" and service "([a-z]+)"')
def check_survey_add_page(step, pk, service):
    step.given('I should be at "%s"' % get_url(Urls.survey_add % (pk, service)))


@step('I should be at "survey_edit" page with pk "(\d+)"')
def check_survey_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.survey_edit % pk))


@step('I should see "survey adding error" message')
def check_survey_adding_error_message(step):
    step.given('I should see "%s"' % Messages.Survey.adding_error)


@step('I should see "survey adding success" message')
def check_survey_adding_success_message(step):
    step.given('I should see "%s"' % Messages.Survey.adding_success)


@step('I should see "survey editing error" message')
def check_survey_editing_error_message(step):
    step.given('I should see "%s"' % Messages.Survey.editing_error)


@step('I should see "survey editing success" message')
def check_survey_editing_success_message(step):
    step.given('I should see "%s"' % Messages.Survey.editing_success)


@step('I close hazard modal')
def close_hazard_modal(step):
    hazard_modal = helper.find(Xpath.hazard_modal)
    helper.check_element_exists(hazard_modal, 'Hazard modal was not found')

    close_button = helper.find(Xpath.modal_close_button, hazard_modal)
    close_button.click()