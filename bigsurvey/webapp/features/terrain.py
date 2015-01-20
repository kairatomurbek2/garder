import datetime
from django.core.management import call_command
from django.conf import settings

from lettuce import before, after, world
from selenium import webdriver


@before.runserver
def initial_setup_db(arg):
    call_command('syncdb', interactive=False, verbosity=1)
    call_command('migrate', interactive=False, verbosity=1)
    call_command('loaddata', 'test', interactive=False, verbosity=1)


@before.all
def initial_setup():
    world.browser = webdriver.Firefox()


@after.all
def teardown_browser(total):
    world.browser.quit()


@before.each_scenario
def clear_cookie(scenario):
    world.browser.delete_all_cookies()


@after.each_scenario
def screenshot_on_error(scenario):
    if scenario.failed:
        world.browser.save_screenshot('tmp/last_failed_scenario_%s.png' % datetime.datetime.now())
        world.browser.delete_all_cookies()