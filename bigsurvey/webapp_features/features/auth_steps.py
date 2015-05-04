from common_steps import *
from lettuce import *
from settings import *
from django.contrib.auth.models import User


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
    try:
        world.user = User.objects.get(username=username)
    except User.DoesNotExist:
        pass


@step('I should be at "home" page')
def check_home_page(step):
    step.given('I should be at "%s"' % get_url(Urls.home))


@step('I should be at "tester home" page')
def check_tester_home_page(step):
    step.given('I should be at "%s"' % get_url(Urls.tester_home))


@step('I should be at "login" page')
def check_login_page(step):
    step.given('I should be at "%s"' % get_url(Urls.login))


@step('I logout')
def logout(step):
    world.user = None
    step.given('I open "%s"' % get_url(Urls.logout))


@step('I logged in as "([-_a-z0-9]+)"')
def logged_in_as(step, role):
    step.given('I open "login" page')
    step.given('I login as "%s"' % role)