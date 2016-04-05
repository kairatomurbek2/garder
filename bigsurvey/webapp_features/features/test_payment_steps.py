from lettuce import step, world
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from main.parameters import Messages
from webapp_features.features import helper
from webapp_features.features.data import get_url, Urls, Xpath, PaypalCredentials


@step('I directly open "unpaid_test_list" page')
def directly_open_unpaid_test_list_page(step):
    step.given('I open "%s"' % get_url(Urls.unpaid_test_list))


@step('I open "unpaid_test_list" page')
def open_unpaid_test_list_page(step):
    step.given('I open "home" page')
    step.given('I click "unpaid_tests" menu link')


@step('I should be on "unpaid_test_list" page')
def check_unpaid_test_list_page(step):
    step.given('I should be at "%s"' % get_url(Urls.unpaid_test_list))


@step('I wait until step 2 is appeared')
def wait_until_step_2_is_appeared(step):
    WebDriverWait(world.browser, 30).until(
        expected_conditions.visibility_of_element_located((By.XPATH, Xpath.payment_step_2))
    )


@step('I login in PayPal')
def login_in_paypal(step):
    import time; time.sleep(6)
    login_button = helper.find(Xpath.Paypal.login_button)
    if login_button:
        login_button.click()
        WebDriverWait(world.browser, 15).until(
            expected_conditions.visibility_of_element_located((By.XPATH, Xpath.Paypal.username))
        )
    username_field = helper.find(Xpath.Paypal.username)
    helper.check_element_exists(username_field, 'Username field was not found')
    username_field.clear()
    username_field.send_keys(PaypalCredentials.username)

    password_field = helper.find(Xpath.Paypal.password)
    helper.check_element_exists(password_field, 'Password field was not found')
    password_field.send_keys(PaypalCredentials.password)

    submit_button = helper.find(Xpath.Paypal.submit_button)
    helper.check_element_exists(submit_button, 'Submit button was not found')
    submit_button.click()


@step('I confirm payment')
def confirm_payment(step):
    continue_button = WebDriverWait(world.browser, 15).until(
        expected_conditions.presence_of_element_located((By.XPATH, Xpath.Paypal.continue_button))
    )
    continue_button.click()


@step('I should be redirected to "unpaid_test_list" page')
def wait_until_redirect(step):
    def check_unpaid_test_list_page(browser):
        return browser.current_url == get_url(Urls.unpaid_test_list)

    WebDriverWait(world.browser, 10).until(check_unpaid_test_list_page)


@step('I should see "payment successful" message')
def check_payment_successful_message(step):
    try:
        step.given('I should see "%s"' % Messages.Test.payment_successful_singular)
    except AssertionError:
        step.given('I should see "%s"' % Messages.Test.payment_successful_plural)


@step('I should see pay modal')
def check_pay_modal_visible(step):
    modal = WebDriverWait(world.browser, 10).until(
        expected_conditions.visibility_of_element_located((By.XPATH, Xpath.pay_modal))
    )
    helper.check_element_exists(modal, 'Payment modal was not found')


@step('I close pay modal')
def close_pay_modal(step):
    modal = helper.find(Xpath.pay_modal)
    helper.check_element_exists(modal, 'Payment modal was not found')

    close_button = helper.find(Xpath.modal_close_button, modal)
    close_button.click()