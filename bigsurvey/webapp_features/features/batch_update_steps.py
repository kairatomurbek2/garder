from lettuce import step, world
from main.parameters import Messages
from webapp_features.features.data import get_url, Urls
from django.core.urlresolvers import reverse


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


@step('I should see "batch updating warning" message')
def check_batch_updating_warning_message(step):
    step.given('I should see "%s"' % Messages.BatchUpdate.hazard_warning[:20])


@step('I should see "batch updating error" message')
def check_batch_updating_error_message(step):
    step.given('I should see "%s"' % Messages.BatchUpdate.error[:20])
