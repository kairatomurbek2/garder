from webapp_features.features.definitions.core import finder
from webapp_features.features.definitions.core.page_interactors import _helper


def assert_that_auditlog_records_are_shown(data):
    _helper.assert_row_exists_in_table(data)


def assert_that_owners_changes_are_not_displayed_in_auditlog():
    xpath = '//tr[contains(.//td[4], "PWSOwners")][contains(.//td[3], "owner")]'
    finder.find_invisible_element_by_xpath(xpath)


def assert_that_owners_changes_are_displayed_in_auditlog():
    xpath = '//tr[contains(.//td[4], "PWSOwners")][contains(.//td[3], "owner")]'
    finder.find_element_by_xpath(xpath)


def assert_that_text_fragment_is_displayed_in_search_result(text):
    xpath = '//tr/td[contains(., "%s")]' % text
    finder.find_element_by_xpath(xpath)


def assert_that_text_fragment_is_not_displayed_in_search_result(text):
    xpath = '//tr/td[contains(., "%s")]' % text
    finder.find_invisible_element_by_xpath(xpath)
