from lettuce import step

from main.parameters import Messages
from webapp import models
from webapp_features.features.common_steps import click_element_by_xpath
from webapp_features.features.data import get_url, Urls, Xpath


@step('I open "invite" page')
def open_invite_page(step):
    step.given('I click "testers" menu link')
    step.given('I click "invite_user" link')


@step('I directly open "invite" page')
def directly_open_invite_page(step):
    step.given('I open "%s"' % get_url(Urls.user_invite))


@step('I should be at "invite" page')
def check_hazard_detail_page(step):
    step.given('I should be at "%s"' % get_url(Urls.user_invite))