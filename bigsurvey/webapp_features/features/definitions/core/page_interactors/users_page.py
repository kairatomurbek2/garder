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


def go_to_surveyor_tab():
    go_to_tab('Surveyors')


def go_to_admins_tab():
    go_to_tab('Administrators')


def assert_edit_link_and_details_link_are_not_displayed_against_user(username, email):
    edit_xpath = './/tr[contains(., "%s")][contains(., "%s")][contains(., "Edit")]' % (username, email)
    detail_xpath = './/tr[contains(., "%s")][contains(., "%s")][contains(., "Detail")]' % (username, email)
    finder.find_invisible_element_by_xpath(edit_xpath)
    finder.find_invisible_element_by_xpath(detail_xpath)


def assert_edit_link_and_details_link_are_displayed_against_user(username, email):
    edit_xpath = './/tr[contains(., "%s")][contains(., "%s")][contains(., "Edit")]' % (username, email)
    detail_xpath = './/tr[contains(., "%s")][contains(., "%s")][contains(., "Detail")]' % (username, email)
    finder.find_element_by_xpath(edit_xpath)
    finder.find_element_by_xpath(detail_xpath)
