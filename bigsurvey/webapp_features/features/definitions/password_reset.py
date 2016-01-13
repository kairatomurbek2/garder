# -*- coding: utf-8 -*-
from lettuce import world, step
from webapp_features.features.definitions.core import common_actions
from webapp_features.features.definitions.core.form_interactors import password_reset_form
from webapp_features.features.definitions.core.navigators import password_reset_navigators
from webapp_features.features.definitions.core.common_actions import read_email
from webapp_features.features.definitions.core.navigators import home_navigator

@step(u'user with email "([^"]*)" reset password from the login page')
def given_user_with_email_reset_password_from_the_login_page(step, email):
    password_reset_navigators.go_to_password_reset_page()
    password_reset_form.enter_email(email)
    password_reset_form.submit()


@step(u'user clicks on a link with a unique token to email')
def when_user_clicks_on_a_link_with_a_unique_token_to_email(step):
    email_obj = read_email()
    message_body = email_obj.body
    url_beginning = message_body.find("127.0.0.1:8000/password/reset/")
    url_end = message_body.find("/\n", url_beginning + 1)
    url = message_body[url_beginning:url_end]
    world.browser.get(url)


@step(u'sets a new password "([^"]*)"')
def and_sets_a_new_password(step, password):
    password_reset_form.enter_new_password(password)
    password_reset_form.submit()


@step(u'user "([^"]*)" and password "([^"]*)" may enter in page')
def then_user_group1_and_password_group2_may_enter_in_page(step, username, password):
    home_navigator.go_to_login_page()
    common_actions.login(username, password)