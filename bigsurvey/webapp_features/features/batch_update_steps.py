from lettuce import step, world
from main.parameters import Messages
from webapp_features.features.data import get_url, Urls
from django.core.urlresolvers import reverse
from django.core.management import call_command
from webapp_features.features.definitions.core import finder

@step('I directly open "batch_update" page')
def directly_open_batch_update_page(step):
    world.browser.get(get_url(Urls.batch_update))


@step('I open "batch_update" page')
def open_batch_update_page(step):
    step.given('I open "home" page')
    step.given('I click "batch_update" menu link')


@step('I should see "batch updating success" message')
def check_batch_updating_success_message(step):
    step.given('I should see "%s"' % Messages.BatchUpdate.success)


@step('I should see "batch updating error" message')
def check_batch_updating_error_message(step):
    step.given('I should see "%s"' % Messages.BatchUpdate.error[:20])


@step(u'There Hazard letters')
def there_hazard_letters(step):
    call_command('loaddata', 'webapp_features/fixtures/hazard_letter_type.json')


@step('I should see "letter creation success" message')
def check_batch_updating_create_latter_success_message(step):
    xpath = '//div[contains(@class, "alert-margin-top uk-alert uk-alert-success")]'
    finder.find_visible_element_by_xpath(xpath)


@step('I should see "letters not created for hazards warning" message')
def check_batch_updating_create_latter_warning_message(step):
    xpath = '//div[contains(@class, "alert-margin-top uk-alert uk-alert-warning")]'
    finder.find_visible_element_by_xpath(xpath)
