from lettuce import step
from webapp_features.features.definitions.core.common_actions import owner_logs_in, admin_logs_in
from webapp_features.features.definitions.core.navigators import home_navigator
from webapp_features.features.definitions.core.page_interactors import pws_page


@step('I logged to system as "(.*)"$')
def log_in(step, username):
    if username == 'owner':
        owner_logs_in()
    if username == 'admin':
        admin_logs_in()


@step('I open PWS page$')
def go_to_pws_page(step):
    home_navigator.go_to_pws_page()


@step('I can see Add PWS button$')
def i_can_see_add_pws_btn(step):
    pws_page.add_pws_btn_is_displayed()


@step('I can not see Add PWS button$')
def i_can_see_add_pws_btn(step):
    pws_page.add_pws_btn_is_not_displayed()
