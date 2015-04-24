from lettuce import *
from selenium.common.exceptions import *
from settings import *


def find(xpath, context=None):
    context = context or world.browser
    try:
        elem = context.find_element_by_xpath(xpath)
    except NoSuchElementException:
        elem = None
    return elem


def find_multiple(xpath, context=None):
    context = context or world.browser
    try:
        elems = context.find_elements_by_xpath(xpath)
    except NoSuchElementException:
        elems = []
    return elems


def check_element_exists(elem, assert_message):
    assert elem, assert_message


def check_element_visible(elem, assert_message):
    assert elem.is_displayed(), assert_message


def check_element_doesnt_exist(elem, assert_message):
    assert not elem, assert_message


def check_text_exists(text, assert_message, context=None):
    context = context or world.browser
    elem = find(Xpath.Pattern.text_inside_element % text, context)
    check_element_exists(elem, assert_message)


def check_text_doesnt_exist(text, assert_message, context=None):
    context = context or world.browser
    elem = find(Xpath.Pattern.text_inside_element % text, context)
    check_element_doesnt_exist(elem, assert_message)