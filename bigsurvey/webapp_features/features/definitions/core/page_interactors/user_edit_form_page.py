from webapp_features.features.definitions.core import finder


def assert_given_group_is_displayed_in_group_selection_form(group_name):
    xpath = './/select[contains(., "%s")]' % group_name
    finder.find_element_by_xpath(xpath)
