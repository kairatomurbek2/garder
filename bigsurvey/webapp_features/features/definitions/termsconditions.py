import os
from django.conf import settings
from lettuce import step
from webapp_features.features.definitions.core.common_actions import root_admin_logs_in
from webapp_features.features.definitions.core.form_interactors import pws_owner_ragistration_form
from webapp_features.features.definitions.core.navigators import admin_navigator
from webapp_features.features.definitions.core.page_interactors import terms_conditions_page


@step('Im on a page to add terms conditions')
def given_im_on_a_page_to_add_terms_conditions(step):
    root_admin_logs_in()
    admin_navigator.go_to_terms_conditions_page_admin()
    admin_navigator.go_to_add_terms_conditions_page_admin()


@step('I submit form')
def and_i_submit_form(step):
    pws_owner_ragistration_form.submit()


@step('I turn to the list of terms conditions')
def when_i_turn_to_the_list_of_terms_conditions(step):
    admin_navigator.go_to_terms_conditions_page_admin()


@step('I see the added file')
def then_i_see_the_added_file(step):
    terms_conditions_page.visible_term_and_condition()


@step('I deleted "(.*)"')
def clear_pdf(step, file):
    pdf = os.path.join(settings.TAC_PDF_DIR, file)
    os.remove(pdf)
    assert not os.path.isfile(pdf), 'File was not deleted'


@step('I see an error "([^"]*)"')
def then_i_see_an_error(step, error):
    terms_conditions_page.see_error(error)
