from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from common_steps import *
from lettuce import *
from settings import *
from webapp.models import TestPermission, Inspection


@step('I directly open "site_list" page')
def directly_open_site_list_page(step):
    step.given('I open "%s"' % get_url(Urls.site_list))


@step('I open "site_list" page')
def open_site_list_page(step):
    step.given('I open "home" page')
    step.given('I click "sites" menu link')


@step('I directly open "site_detail" page with pk "(\d+)"')
def directly_open_site_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.site_detail % pk))


@step('I open "site_detail" page with pk "(\d+)"')
def open_site_detail_page(step, pk):
    step.given('I open "site_list" page')
    step.given('I click "site_%s_detail" link' % pk)


@step('I directly open "site_add" page')
def directly_open_site_add_page(step):
    step.given('I open "%s"' % get_url(Urls.site_add))


@step('I open "site_add" page')
def open_site_add_page(step):
    step.given('I open "site_list" page')
    step.given('I click "site_add" link')


@step('I directly open "site_edit" page with pk "(\d+)"')
def directly_open_site_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.site_edit % pk))


@step('I open "site_edit" page with pk "(\d+)"')
def open_site_edit_page(step, pk):
    step.given('I open "site_detail" page with pk "%s"' % pk)
    step.given('I click "site_%s_edit" link' % pk)


@step('I should be at "site_list" page')
def check_site_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.site_list))


@step('I should be at "site_add" page')
def check_site_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.site_add))


@step('I should be at "site_edit" page with pk "(\d+)"')
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


@step('I should see "site adding success" message')
def check_site_adding_success_message(step):
    step.given('I should see "%s"' % Messages.Site.adding_success)


@step('I should see "site adding error" message')
def check_site_adding_error_message(step):
    step.given('I should see "%s"' % Messages.Site.adding_error)


@step('I should see "site editing success" message')
def check_site_editing_success_message(step):
    step.given('I should see "%s"' % Messages.Site.editing_success)


@step('I should see "site editing error" message')
def check_site_editing_error_message(step):
    step.given('I should see "%s"' % Messages.Site.editing_error)


@step('I open select customer modal')
def open_customer_selector(step):
    click_button_with_label(step, "Select Customer")


@step('I select customer with pk "(\d+)"')
def select_customer(step, pk):
    select_button = helper.find(Xpath.Pattern.customer_select_button % pk)
    helper.check_element_exists(select_button, 'Customer select button with pk "%s" was not found' % pk)
    select_button.click()


@step('I commit site')
def commit_site(step):
    commit_dialog_button = helper.find(Xpath.commit_dialog_button)
    helper.check_element_exists(commit_dialog_button, 'Commit dialog button was not found')
    commit_dialog_button.click()
    commit_button = helper.find(By.XPATH, Xpath.Pattern.submit_button)
    helper.check_element_exists(commit_button, 'Commit dialog button was not found')
    commit_button.click()


@step("Uncommit sites")
def uncommit_sites(step):
    Inspection.objects.all().update(is_active=True)
    TestPermission.objects.all().update(is_active=True)


@step('I hover on "assign" link')
def hover_on_menu(step):
    assign_link = helper.find(Xpath.Pattern.link % 'assign')
    helper.check_element_exists(assign_link, 'Assign link was not found')
    actions = ActionChains(world.browser)
    actions.move_to_element(assign_link).perform()