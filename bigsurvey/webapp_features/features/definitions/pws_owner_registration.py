# -*- coding: utf-8 -*-
from lettuce import step, world
from django.core.management import call_command
from main.parameters import Messages
from selenium.webdriver.support.wait import WebDriverWait
from webapp_features.features.data import get_url, Urls
from webapp_features.features.definitions.core import common_actions
from webapp_features.features.definitions.core.navigators import pws_owner_registration_navigators
from webapp_features.features.definitions.core.form_interactors import pws_owner_ragistration_form
from webapp_features.features.definitions.core.page_interactors import sites_page


@step(u'I register as PWS owner with following data')
def given_i_register_as_pws_owner_with_following_data(step):
    pws_owner_registration_navigators.go_to_registration_page()
    pws_owner_ragistration_form.fill_in_multiple_textfields(step)
    pws_owner_ragistration_form.checkbox_click()
    pws_owner_ragistration_form.submit()


@step(u'I authenticate with "([^"]*)" "([^"]*)"')
def and_i_authenticate_with_login_password(step, username, password):
    common_actions.login(username, password)


@step(u'I See the list of following sites')
def then_i_see_the_list_of_following_sites(step):
    sites_page.following_sites()


@step(u'The system has data for the demo trial')
def given_the_system_has_data_for_the_demo_trial(step):
    call_command('loaddata', 'webapp_features/fixtures/pws_owner_registration.json')


@step(u'I click Pay and activate button')
def and_i_click_group_button(step):
    pws_owner_registration_navigators.go_to_activate_page()
    sites_page.click_pay_button()


@step(u'I should be redirected to "site" page')
def then_i_should_be_redirected_to_page(step):
    def check_site_list_page(browser):
        return browser.current_url == get_url(Urls.site_list)

    WebDriverWait(world.browser, 10).until(check_site_list_page)


@step(u'I should see "payment was completed successfully" message')
def and_i_should_see_group1_message(step):
    try:
        step.given('I should see "%s"' % Messages.PWS.payment_successful_singular)
    except AssertionError:
        step.given('I should see "%s"' % Messages.PWS.payment_successful_plural)
