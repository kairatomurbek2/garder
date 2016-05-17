from webapp_features.features.definitions.core import finder


def visible_term_and_condition():
    xpath = '//th[contains(@class, "field-__str__")]'
    finder.find_element_by_xpath(xpath)


def see_error(error):
    xpath = '//ul[@class="errorlist"]//li[contains(text(), "%s")]' % error
    finder.find_element_by_xpath(xpath)
