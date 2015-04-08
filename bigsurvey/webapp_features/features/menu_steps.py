from selenium.webdriver import ActionChains
from common_steps import *
from lettuce import *
from settings import *


@step('I should see following menu links')
def check_menu_links_exist(step):
    for row in step.hashes:
        link = helper.find(Xpath.Pattern.menu_item % row['link'])
        helper.check_element_exists(link, '"%s" link is not in menu' % row['link'])


@step('I should not see following menu links')
def check_menu_links_dont_exist(step):
    for row in step.hashes:
        link = helper.find(Xpath.Pattern.menu_item % row['link'])
        helper.check_element_doesnt_exist(link, '"%s" link is in menu' % row['link'])


@step('I hover on "more" link')
def hover_on_menu(step):
    menu = helper.find(Xpath.more_link)
    helper.check_element_exists(menu, 'Menu link was not found')
    actions = ActionChains(world.browser)
    actions.move_to_element(menu).perform()


@step('I click "([-_a-z0-9]+)" menu link')
def click_menu_link(step, link_name):
    step.given('I hover on "menu" link')
    link = helper.find(Xpath.Pattern.menu_item % link_name)
    helper.check_element_exists(link, '"%s" link is not in menu' % link_name)
    link.click()

@step('I click "([-_a-z0-9]+)" outer menu link')
def click_outer_menu_link(step, link_name):
    link = helper.find(Xpath.Pattern.menu_item % link_name)
    helper.check_element_exists(link, '"%s" link is not in menu' % link_name)
    link.click()