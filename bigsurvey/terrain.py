from datetime import datetime

from django.conf import settings
from django.core.management import call_command
from lettuce import before, after, world
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


@before.all
def init():
    try:
        call_command('flush', interactive=False, verbosity=1)
        call_command('reset_autoincrement')
    except RuntimeError:
        pass
    call_command('migrate', interactive=False, verbosity=1, load_initial_data=False)
    call_command('restore_db', interactive=False, verbosity=1)
    call_command('createinitialrevisions', interactive=False, verbosity=1)
    world.browser = webdriver.Firefox(webdriver.FirefoxProfile(settings.FIREFOX_PROFILE_DIR))
    world.browser.maximize_window()
    world.browser.implicitly_wait(1)
    world.user = None
    world.cache = {}
    world.wait = WebDriverWait(world.browser, 20)


@after.all
def teardown(total):
    world.browser.quit()


@after.each_scenario
@after.outline
def clear_cookies_and_db(scenario, *args, **kwargs):
    world.browser.delete_all_cookies()
    if settings.REINITIALIZE_DATABASE and 'keep_db' not in scenario.tags:
        call_command('restore_db', interactive=False, verbosity=0)
        call_command('createinitialrevisions', interactive=False, verbosity=1)
        call_command('reset_autoincrement')
    world.user = None
    world.cache = {}


@after.each_scenario
@after.outline
def take_screenshot(scenario, *args, **kwargs):
    if scenario.failed:
        date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        world.browser.get_screenshot_as_file('/home/itattractor/failed_tests/screens/%s-%s.png' % (date, scenario.name.replace(' ', '-')))
