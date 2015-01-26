from lettuce import *
from selenium.common.exceptions import *


def find_elem_by_xpath(xpath, context=None):
    context = context or world.browser
    try:
        elem = context.find_element_by_xpath(xpath)
    except NoSuchElementException:
        elem = None
    return elem