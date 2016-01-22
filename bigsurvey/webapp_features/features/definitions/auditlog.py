from django.core.management import call_command
from lettuce import step
from webapp_features.features.definitions.core import common_actions
from webapp_features.features.definitions.core import finder
from webapp_features.features.definitions.core.form_interactors import (
    user_edit_form, site_form, auditlog_form
)
from webapp_features.features.definitions.core.navigators import home_navigator
from webapp_features.features.definitions.core.page_interactors import (
    users_page, auditlog_page, sites_page
)


@step('Owner of the following PWSs changes username of "(.*)" user to "(.*)":')
def pws_owner_changes_tester_username(step, old_username, new_username):
    upload_initial_data()
    common_actions.login('owner2', 'admin')
    home_navigator.go_to_users_page()
    users_page.go_to_testers_tab()
    users_page.open_user_edit_form(old_username)
    user_edit_form.change_username(new_username)


def upload_initial_data():
    call_command('loaddata', 'webapp_features/fixtures/pws_owner_and_tester.json')
    call_command('createinitialrevisions', model_class='PWS')
    call_command('createinitialrevisions', model_class='User')
    call_command('createinitialrevisions', model_class='Employee')


@step(u'When Owner of the following PWSs goes to auditlog page:')
def when_owner_of_the_following_pwss_goes_to_auditlog_page(step):
    common_actions.owner_logs_in()
    home_navigator.go_to_auditlog_page()


@step(u'Then there are no auditlog records displayed on the page')
def then_there_are_no_auditlog_records_displayed_on_the_page(step):
    finder.find_invisible_element_by_xpath('.//tbody/tr')


@step(u'But Owner of the following PWSs goes to auditlog page:')
def but_owner_of_the_following_pwss_goes_to_auditlog_page(step):
    common_actions.login('owner2', 'admin')
    home_navigator.go_to_auditlog_page()


@step(u'And sees the following record:')
def and_sees_the_following_record(step):
    table = step.hashes[0]
    auditlog_page.assert_that_auditlog_records_are_shown(table)


@step(u'Given surveyor edited site "([^"]*)"$')
def given_surveyor_edited_site_group1(step, site_account_number):
    common_actions.surveyor_logs_in()
    _edit_site(site_account_number)


@step(u'And owner edited site "([^"]*)"$')
def given_surveyor_edited_site_group1(step, site_account_number):
    common_actions.owner_logs_in()
    _edit_site(site_account_number)


def _edit_site(site_account_number):
    sites_page.open_site_for_editing(site_account_number)
    site_form.select_yes_in_fire_present()
    site_form.submit_form()


@step(u'When owner filters auditlog by username "([^"]*)"')
def when_owner_filters_auditlog_by_username_group1(step, username):
    home_navigator.go_to_auditlog_page()
    auditlog_form.filter_by_username(username)


@step(u'Then he sees the following record:')
def then_he_sees_the_following_record(step):
    table = step.hashes[0]
    auditlog_page.assert_that_auditlog_records_are_shown(table)


@step(u'But does not see changes made by owner')
def does_not_see_owner_changes(step):
    auditlog_page.assert_that_owners_changes_are_not_displayed_in_auditlog()
