from common_steps import *
from lettuce import *
from settings import *


@step('I open "login" page')
def open_login_page(step):
    step.given('I open "%s"' % get_url(Urls.login))


@step('I login as "root"')
def login_as_root(step):
    step.given('I login with username "%s" and password "%s"' % (Logins.root['username'], Logins.root['password']))


@step('I login as "admin"')
def login_as_root(step):
    step.given('I login with username "%s" and password "%s"' % (Logins.admin['username'], Logins.admin['password']))


@step('I login as "surveyor"')
def login_as_root(step):
    step.given('I login with username "%s" and password "%s"' % (Logins.surveyor['username'], Logins.surveyor['password']))


@step('I login as "tester"')
def login_as_root(step):
    step.given('I login with username "%s" and password "%s"' % (Logins.tester['username'], Logins.tester['password']))


@step('I login as "non existent user"')
def login_as_root(step):
    step.given('I login with username "%s" and password "%s"' % (Logins.non_existent_user['username'], Logins.non_existent_user['password']))


@step('I login with username "(.*)" and password "(.*)"')
def login(step, username, password):
    step.given('I fill in "username" with "%s"' % username)
    step.given('I fill in "password" with "%s"' % password)
    step.given('I submit "%s" form' % 'auth')


@step('I should be at "home" page')
def check_home_page(step):
    step.given('I should be at "%s"' % get_url(Urls.home))


@step('I should be at "login" page')
def check_login_page(step):
    step.given('I should be at "%s"' % get_url(Urls.login))


@step('I log out')
def logout(step):
    step.given('I open "%s"' % get_url(Urls.logout))