from common_steps import *
from lettuce import *
from settings import *
from webapp.models import Hazard


@step('I directly open "hazard_detail" page with pk "(\d+)"')
def directly_open_hazard_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.hazard_detail % pk))


@step('I open "hazard_detail" page with pk "(\d+)"')
def open_hazard_detail_page(step, pk):
    survey = Hazard.objects.get(pk=pk).survey
    if world.user.has_perm('webapp.browse_survey'):
        step.given('I open "survey_detail" page with pk "%s"' % survey.pk)
    else:
        step.given('I open "site_detail" page with pk "%s"' % survey.site.pk)
        step.given('I click "%s" link' % survey.service_type.service_type)
    step.given('I click "hazard_%s_detail" link' % pk)


@step('I directly open "hazard_add" page for survey with pk "(\d+)"')
def directly_open_hazard_add_page_for_site(step, survey_pk):
    step.given('I open "%s"' % get_url(Urls.hazard_add % survey_pk))


@step('I open "hazard_add" page for survey with pk "(\d+)"')
def open_hazard_add_page_for_site(step, survey_pk):
    step.given('I open "survey_detail" page with pk "%s"' % survey_pk)
    step.given('I click "survey_%s_hazard_add" link' % survey_pk)


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


@step('I should be at "hazard_add" page for survey with pk "(\d+)"')
def check_hazard_add_page(step, survey_pk):
    step.given('I should be at "%s"' % get_url(Urls.hazard_add % survey_pk))


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