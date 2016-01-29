from django.core.management import call_command
from lettuce import step
from webapp_features.features.definitions.core.common_actions import owner_logs_in, admin_logs_in
from webapp_features.features.definitions.core.navigators import home_navigator
from webapp_features.features.definitions.core.page_interactors.user_edit_form_page import \
    assert_given_group_is_displayed_in_group_selection_form
from webapp_features.features.definitions.core.page_interactors.users_page import (
    go_to_tab, open_user_edit_form, go_to_admins_tab, assert_edit_link_and_details_link_are_not_displayed_against_user,
    assert_edit_link_and_details_link_are_displayed_against_user
)

@step('I logged in as pws owner$')
def log_in_as_owner(step):
    owner_logs_in()


@step('I logged in as pws admin$')
def log_in_as_admin(step):
    admin_logs_in()


@step('There is another_admin user in Adminstrators group')
def another_admin(step):
    call_command('loaddata', 'webapp_features/fixtures/another_admin.json')


@step('I open user adding form$')
def open_user_adding_form(step):
    home_navigator.go_to_user_edit_form()


@step('I see the following user groups to choose from:$')
def see_user_groups_to_choose_from(step):
    for row in step.hashes:
        assert_given_group_is_displayed_in_group_selection_form(row['group'])


@step('I open Administrators tab on users page$')
def open_administrators_tab(step):
    home_navigator.go_to_users_page()
    go_to_admins_tab()


@step('I open editing form of "(.*)" from usergroup "(.*)"$')
def open_user_editing_form(step, user, group):
    home_navigator.go_to_users_page()
    go_to_tab(group)
    open_user_edit_form(user)


@step('I do not see action links against user "(.*)" with email "(.*)"$')
def i_do_not_see_links_against_user(step, username, email):
    assert_edit_link_and_details_link_are_not_displayed_against_user(username, email)


@step('But I see action links against user "(.*)" with email "(.*)"$')
def i_see_links_against_user(step, username, email):
    assert_edit_link_and_details_link_are_displayed_against_user(username, email)
