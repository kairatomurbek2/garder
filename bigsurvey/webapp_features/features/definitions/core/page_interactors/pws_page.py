from webapp_features.features.definitions.core import finder


_ADD_PWS_BTN_XPATH = './/ul/li/a[contains(., "Add PWS")]'


def add_pws_btn_is_displayed():
    finder.find_element_by_xpath(_ADD_PWS_BTN_XPATH)


def add_pws_btn_is_not_displayed():
    finder.find_invisible_element_by_xpath(_ADD_PWS_BTN_XPATH)
