from lettuce import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

from webapp_features.features.data import Xpath

menu, is_top_menu = None, False
browser_width, browser_height = None, None


def get_browser_size():
    size = world.browser.get_window_size()
    return size['width'], size['height']


def get_menu_context():
    """
    Returns menu context.
    Firstly tries to get top menu
    If it is not visible then falls back to canvas menu
    :rtype tuple(WebElement, bool)
    """
    global browser_width, browser_height, menu, is_top_menu
    width, height = get_browser_size()
    if menu and browser_width == width and browser_height == height:
        return menu
    try:
        top_menu = find(Xpath.top_menu)
        if top_menu.is_displayed():
            menu = top_menu
            is_top_menu = True
            return menu, is_top_menu
        raise ElementNotVisibleException
    except ElementNotVisibleException:
        canvas_menu = find(Xpath.canvas_menu)
        menu = canvas_menu
        is_top_menu = False
        return menu, is_top_menu


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


def check_element_not_visible(elem, assert_message):
    assert not elem or not elem.is_displayed(), assert_message


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


def check_text_exists_inside_element(xpath, text, assert_message, context=None):
    context = context or world.browser
    elem = find(xpath, context)
    check_element_exists(elem, 'Element with xpath "%s" was not found' % xpath)
    assert text in elem.text, assert_message


def check_text_doesnt_exist_inside_element(xpath, text, assert_message, context=None):
    context = context or world.browser
    elem = find(xpath, context)
    check_element_exists(elem, 'Element with xpath "%s" was not found' % xpath)
    assert text not in elem.text, assert_message
