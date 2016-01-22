import datetime

from dateutil.relativedelta import relativedelta
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

TODAY = datetime.date.today()
FIRST_DAY_OF_CUR_MONTH = TODAY - datetime.timedelta(days=TODAY.day - 1)


@step('Owner of the following PWSs changes username of tester "(.*)" user to "(.*)":')
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


@step(u'When owner filters auditlog by username "([^"]*)"$')
def when_owner_filters_auditlog_by_username(step, username):
    home_navigator.go_to_auditlog_page()
    auditlog_form.filter_by_username(username)


@step(u'When owner filters auditlog by user group "([^"]*)"$')
def when_owner_filters_auditlog_by_user_group(step, user_group):
    home_navigator.go_to_auditlog_page()
    auditlog_form.filter_by_user_group(user_group)


@step(u'When owner filters auditlog by record object "([^"]*)"$')
def when_owner_filters_auditlog_by_record_object(step, record_object_text_fragment):
    home_navigator.go_to_auditlog_page()
    auditlog_form.filter_by_record_object(record_object_text_fragment)


@step(u'When owner filters auditlog from current month start to current month end$')
def when_owner_filters_from_current_month_start_to_current_month_end(step):
    last_day_of_cur_month = FIRST_DAY_OF_CUR_MONTH + relativedelta(months=1, days=-1)
    start_date_str = FIRST_DAY_OF_CUR_MONTH.strftime("%Y-%m-%d")
    end_date_str = last_day_of_cur_month.strftime("%Y-%m-%d")

    home_navigator.go_to_auditlog_page()
    auditlog_form.filter_by_date_range(start_date_str, end_date_str)


@step(u'When owner filters auditlog from next month start to next month end$')
def when_owner_filters_from_current_month_start_to_current_month_end(step):
    first_day_of_next_month = FIRST_DAY_OF_CUR_MONTH + relativedelta(months=1)
    last_day_of_next_month = first_day_of_next_month + relativedelta(months=1, days=-1)
    start_date_str = first_day_of_next_month.strftime("%Y-%m-%d")
    end_date_str = last_day_of_next_month.strftime("%Y-%m-%d")

    home_navigator.go_to_auditlog_page()
    auditlog_form.filter_by_date_range(start_date_str, end_date_str)


@step(u'Then he sees the following record:$')
def then_he_sees_the_following_record(step):
    table = step.hashes[0]
    auditlog_page.assert_that_auditlog_records_are_shown(table)


@step(u'Then he sees the following text in search results: "([^"]*)"$')
def sees_text_in_search_results(step, text):
    auditlog_page.assert_that_text_fragment_is_displayed_in_search_result(text)


@step(u'But does not see changes made by owner$')
def does_not_see_owner_changes(step):
    auditlog_page.assert_that_owners_changes_are_not_displayed_in_auditlog()


@step(u'And sees changes made by owner$')
def sees_changes_made_by_owner(step):
    auditlog_page.assert_that_owners_changes_are_displayed_in_auditlog()


@step(u'Given owner owns two PWSs and changes surveyors usernames:')
def given_owner_owns_two_pwss_and_changes_surveyors_usernames(step):
    common_actions.owner_logs_in()
    table = step.hashes
    for row in table:
        home_navigator.go_to_users_page()
        users_page.go_to_surveyor_tab()
        users_page.open_user_edit_form(row['Surveyor old username'])
        user_edit_form.change_username(row['Surveyor new username'])


@step(u'When owner filters auditlog records by PWS "([^"]*)"')
def when_owner_filters_auditlog_records_by_pws(step, pws):
    home_navigator.go_to_auditlog_page()
    auditlog_form.filter_by_pws(pws)


@step(u'Then owner sees "([^"]*)" in the search results$')
def then_owner_sees_group1_in_the_search_results(step, text_value):
    auditlog_page.assert_that_text_fragment_is_displayed_in_search_result(text_value)


@step(u'But owner does not see "([^"]*)" in the search results$')
def but_owner_does_not_see_group1_in_the_search_results(step, text_value):
    auditlog_page.assert_that_text_fragment_is_not_displayed_in_search_result(text_value)
