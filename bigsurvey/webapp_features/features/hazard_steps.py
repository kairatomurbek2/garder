from lettuce import step

from main.parameters import Messages
from webapp import models
from webapp_features.features.common_steps import click_element_by_xpath
from webapp_features.features.data import get_url, Urls, Xpath


@step('I open "hazard_list" page')
def open_hazard_list_page(step):
    step.given('I click "hazards" menu link')


@step('I directly open "hazard_detail" page with pk "(\d+)"')
def directly_open_hazard_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.hazard_detail % pk))


@step('I open "hazard_detail" page with pk "(\d+)"')
def open_hazard_detail_page(step, pk):
    step.given('I open "hazard_list" page')
    step.given('I click "hazard_%s_detail" link' % pk)


@step('I directly open "hazard_add" page for site with pk "(\d+)" and service "([a-z]+)"')
def directly_open_hazard_add_page_for_site(step, survey_pk, service_name):
    step.given('I open "%s"' % get_url(Urls.hazard_add % (survey_pk, service_name)))


@step('I open "hazard_add" page for site with pk "(\d+)" and service "([a-z]+)"')
def open_hazard_add_page_for_site(step, survey_pk, service_name):
    step.given('I open "site_detail" page with pk "%s"' % survey_pk)
    click_element_by_xpath(Xpath.Pattern.site_hazards_button)
    step.given('I click "h%s" link' % service_name)
    step.given('I click "site_%s_hazard_add" link' % service_name)


@step('I directly open "hazard_edit" page with pk "(\d+)"')
def directly_open_hazard_add_page_for_site(step, pk):
    step.given('I open "%s"' % get_url(Urls.hazard_edit % pk))


@step('I open "hazard_edit" page with pk "(\d+)"$')
def open_hazard_edit_page(step, pk):
    step.given('I open "hazard_detail" page with pk "%s"' % pk)
    step.given('I click "hazard_%s_edit" link' % pk)


@step('I should be at "hazard_detail" page with pk "(\d+)"')
def check_hazard_detail_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.hazard_detail % pk))


@step('I should be at "hazard_add" page for survey with pk "(\d+)" and service "([a-z]+)"')
def check_hazard_add_page(step, survey_pk, service_name):
    step.given('I should be at "%s"' % get_url(Urls.hazard_add % (survey_pk, service_name)))


@step('I should be at "hazard_edit" page with pk "(\d+)"')
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


@step('"(.*)" (has|does not have) licence for installation')
def set_has_licence_for_installation(step, username, relation):
    user = models.User.objects.get(username=username)
    has_licence_for_installation = True if relation == 'has' else False
    user.employee.has_licence_for_installation = has_licence_for_installation
    user.employee.save()