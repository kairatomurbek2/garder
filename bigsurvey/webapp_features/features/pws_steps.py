from common_steps import *
from lettuce import *
from settings import *


@step('I open "pws list" page')
def open_pws_list_page(step):
    step.given('I open "%s"' % get_url(Urls.pws_list))


@step('I open "pws add" page')
def open_pws_add_page(step):
    step.given('I open "%s"' % get_url(Urls.pws_add))


@step('I open "pws edit" page with pk "(\d+)"')
def open_pws_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.pws_edit % pk))


@step('I should be at "pws list" page')
def check_pws_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.pws_list))


@step('I should be at "pws add" page')
def check_pws_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.pws_add))


@step('I should be at "pws edit" page with pk "(\d+)"')
def check_pws_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.pws_edit % pk))
