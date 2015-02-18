from django.core.management import call_command
from lettuce import before, after, world
from selenium import webdriver


@before.all
def init():
    call_command('reset_db', interactive=False, verbosity=1)
    call_command('migrate', interactive=False, verbosity=1, load_initial_data=False)
    call_command('loaddata', 'test', interactive=False, verbosity=1)
    world.browser = webdriver.Firefox()
    world.browser.maximize_window()


@after.all
def teardown(total):
    world.browser.quit()


@before.each_scenario
@after.each_scenario
def clear_cookies(scenario):
    world.browser.delete_all_cookies()
    world.user = None