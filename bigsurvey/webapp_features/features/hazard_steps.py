from common_steps import *
from lettuce import *
from settings import *


@step('I open "hazard detail" page with pk "(\d+)"')
def open_hazard_detail_page(step, hazard_pk):
    step.given('I open "%s"' % get_url(Urls.hazard_detail % hazard_pk))


@step('I open "hazard add" page for survey with pk "(\d+)"')
def open_hazard_add_page_for_site(step, survey):
    step.given('I open "%s"' % get_url(Urls.hazard_add % survey))


@step('I open "hazard edit" page with pk "(\d+)"')
def open_hazard_add_page_for_site(step, site_pk):
    step.given('I open "%s"' % get_url(Urls.hazard_edit % site_pk))


@step('I should be at "hazard detail" page with pk "(\d+)"')
def check_hazard_detail_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.hazard_detail % pk))


@step('I should be at "hazard add" page for survey with pk "(\d+)"')
def check_hazard_add_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.hazard_add % pk))


@step('I should be at "hazard edit" page with pk "(\d+)"')
def check_site_detail_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.hazard_edit % pk))


@step('I should see "hazard adding error" message')
def check_hazard_adding_error_message(step):
    step.given('I should see "%s"' % Messages.Hazard.adding_error)


@step('I should see "hazard adding success" message')
def check_hazard_adding_success_message(step):
    step.given('I should see "%s"' % Messages.Hazard.adding_success)


@step('I should see "hazard editing error" message')
def check_hazard_editing_error_message(step):
    step.given('I should see "%s"' % Messages.Hazard.editing_error)


@step('I should see "hazard editing success" message')
def check_hazard_editing_success_message(step):
    step.given('I should see "%s"' % Messages.Hazard.editing_success)