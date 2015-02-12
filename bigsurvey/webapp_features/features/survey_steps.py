from common_steps import *
from lettuce import *
from settings import *


@step('I open "survey detail" page with pk "(\d+)"')
def open_survey_detail_page(step, survey_pk):
    step.given('I open "%s"' % get_url(Urls.survey_detail % survey_pk))

@step('I open "survey add" page for site with pk "(\d+)" and service "([a-z]+)"')
def open_survey_add_page_for_site(step, site_pk, service_type):
    step.given('I open "%s"' % get_url(Urls.survey_add % (site_pk, service_type)))

@step('I open "survey edit" page with pk "(\d+)"')
def open_survey_add_page_for_site(step, site_pk):
    step.given('I open "%s"' % get_url(Urls.survey_edit % site_pk))

@step('I should be at "survey detail" page with pk "(\d+)"')
def check_site_detail_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.survey_detail % pk))

@step('I should be at "survey add" page for site with pk "(\d+)" and service "([a-z]+)"')
def check_survey_add_page(step, pk, service):
    step.given('I should be at "%s"' % get_url(Urls.survey_add % (pk, service)))

@step('I should be at "survey edit" page with pk "(\d+)"')
def check_site_detail_page(step, pk):
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