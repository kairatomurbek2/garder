from django.core.management import call_command
from lettuce import step
from webapp_features.features.definitions.core import common_actions
from webapp_features.features.definitions.core import finder
from webapp_features.features.definitions.core.navigators import home_navigator
from webapp_features.features.definitions.core.page_interactors import users_page, auditlog_page
from webapp_features.features.definitions.core.form_interactors import user_edit_form


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
