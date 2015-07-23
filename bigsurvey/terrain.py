from datetime import datetime

from django.core.management import call_command
from lettuce import before, after, world
from selenium import webdriver


@before.all
def init():
    call_command('reset_db', interactive=False, verbosity=1)
    call_command('migrate', interactive=False, verbosity=1, load_initial_data=False)
    call_command('restore_db', interactive=False, verbosity=1)
    world.browser = webdriver.Firefox()
    world.browser.maximize_window()
    world.browser.implicitly_wait(1)
    world.user = None
    world.cache = {}


@after.all
def teardown(total):
    world.browser.quit()


@before.each_scenario
@before.outline
def clear_cookies_and_db(scenario):
    world.browser.delete_all_cookies()
    call_command('restore_db', interactive=False, verbosity=0)
    world.user = None
    world.cache = {}


@after.each_scenario
def take_screenshot(scenario):
    if scenario.failed:
        date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        world.browser.get_screenshot_as_file('/home/itattractor/failed_tests/screens/%s-%s.png' % (date, scenario.name.replace(' ', '-')))
