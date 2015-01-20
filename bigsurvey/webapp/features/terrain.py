import datetime
from django.core.management import call_command

from lettuce import before, after, world
from selenium import webdriver


@before.all
def initial_setup():
    call_command('reset_db', interactive=False, verbosity=1)
    call_command('syncdb', interactive=False, verbosity=1)
    call_command('migrate', interactive=False, verbosity=1)
    call_command('loaddata', 'test', interactive=False, verbosity=1)
    world.browser = webdriver.Firefox()
    world.browser.maximize_window()


@after.all
def teardown_browser(total):
    call_command('reset_db', interactive=False, verbosity=1)
    world.browser.quit()


@before.each_scenario
def clear_cookie(scenario):
    world.browser.delete_all_cookies()


@after.each_scenario
def screenshot_on_error(scenario):
    if scenario.failed:
        world.browser.save_screenshot('tmp/last_failed_scenario_%s.png' % datetime.datetime.now())