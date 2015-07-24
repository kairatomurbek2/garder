from selenium.webdriver import ActionChains
from lettuce import step, world
from webapp_features.features import helper
from webapp_features.features.data import Xpath


@step('I should see following menu links')
def check_menu_links_exist(step):
    step.given('I click on "more" link')
    menu, is_top_menu = helper.get_menu_context()
    for row in step.hashes:
        link = helper.find(Xpath.Pattern.menu_item % row['link'], menu)
        helper.check_element_visible(link, '"%s" link is not visible in menu' % row['link'])


@step('I should not see following menu links')
def check_menu_links_dont_exist(step):
    step.given('I click on "more" link')
    menu, is_top_menu = helper.get_menu_context()
    for row in step.hashes:
        link = helper.find(Xpath.Pattern.menu_item % row['link'], menu)
        helper.check_element_not_visible(link, '"%s" link is visible in menu' % row['link'])


@step('I open offcanvas menu')
def open_offcanvas_menu(step):
    step.given('I click "#offcanvas" link')


@step('I click on "more" link')
def click_on_more_link(step):
    menu, is_top_menu = helper.get_menu_context()
    more_link = helper.find(Xpath.more_link, menu)
    if not is_top_menu:
        step.given('I open offcanvas menu')
    try:
        helper.check_element_exists(more_link, '"More" menu link was not found')
        if is_top_menu:
            actions = ActionChains(world.browser)
            actions.move_to_element(more_link).perform()
        else:
            more_link.click()
    except AssertionError:
        return


@step('I click "([-_a-z0-9]+)" menu link')
def click_menu_link(step, link_name):
    step.given('I click on "more" link')
    menu, is_top_menu = helper.get_menu_context()
    link = helper.find(Xpath.Pattern.menu_item % link_name, menu)
    helper.check_element_exists(link, '"%s" link is not in menu' % link_name)
    link.click()
