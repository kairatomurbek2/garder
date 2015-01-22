from common_steps import *
from lettuce import *
from webapp.features.test_data import *


@step('I login as (.*)')
def login_as(step, role):
    requisites = TestData.logins[role]
    login(step, requisites['username'], requisites['password'])


@step('Login with username (.*) and password (.*)')
def login(step, username, password):
    fill_field_with_value(step, 'auth_username', username)
    fill_field_with_value(step, 'auth_password', password)
    submit_form(step, 'auth')