from common_steps import *
from lettuce import *
from settings import *


@step('I login as "([a-z0-9_]+)"')
def login_as(step, role):
    requisites = LOGINS[role]
    step.given('I login with username "%s" and password "%s"' % (requisites['username'], requisites['password']))


@step('I login with username "(.*)" and password "(.*)"')
def login(step, username, password):
    fill_in_textfield(step, 'auth_username', username)
    fill_in_textfield(step, 'auth_password', password)
    step.given('I submit "%s" form' % 'auth')