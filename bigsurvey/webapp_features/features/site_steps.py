from common_steps import *
from lettuce import *
from settings import *


@step('I open "site list" page')
def open_site_list_page(step):
    step.given('I open "%s"' % get_url(Urls.site_list))


@step('I open "site detail" page with pk "(\d+)"')
def open_site_list_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.site_detail % pk))


@step('I open "site add" page')
def open_site_add_page(step):
    step.given('I open "%s"' % get_url(Urls.site_add))


@step('I open "site edit" page with pk "(\d+)"')
def open_site_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.site_edit % pk))


@step('I should be at "site list" page')
def check_site_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.site_list))


@step('I should be at "site add" page')
def check_site_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.site_add))


@step('I should be at "site edit" page with pk "(\d+)"')
def check_site_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.site_edit % pk))


@step('I should see following text in following services')
def check_text_in_services_exists(step):
    for row in step.hashes:
        elem = helper.find(Xpath.Pattern.site_service % row['service'])
        helper.check_element_exists(elem, 'service "%s" was not found' % row['service'])
        helper.check_text_exists(row['text'], '"%s" is not in "%s" service' % (row['text'], row['service']), elem)


@step('I should not see following text in following services')
def check_text_in_services_doesnt_exist(step):
    for row in step.hashes:
        elem = helper.find(Xpath.Pattern.site_service % row['service'])
        helper.check_element_exists(elem, 'service "%s" was not found' % row['service'])
        helper.check_text_doesnt_exist(row['text'], '"%s" is in "%s" service' % (row['text'], row['service']), elem)