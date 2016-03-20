# -*- coding: utf-8 -*-
from lettuce import step
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
