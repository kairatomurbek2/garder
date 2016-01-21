from webapp_features.features.definitions.core import finder


def go_to_tab(tab_text):
    tab_xpath = './/a[@class="uk-text-large"][contains(., "%s")]' % tab_text
    tab = finder.find_element_by_xpath(tab_xpath)
    tab.click()


def go_to_testers_tab():
    go_to_tab('Testers')


def open_user_edit_form(username):
    user_row_xpath = ".//tr[contains(., '%s')]/td/a[contains(.,'Edit')]" % username
    user_edit_link = finder.find_element_by_xpath(user_row_xpath)
    user_edit_link.click()

