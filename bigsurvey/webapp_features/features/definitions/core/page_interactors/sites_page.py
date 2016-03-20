from webapp_features.features.definitions.core import finder
from webapp_features.features.definitions.core.navigators import home_navigator


def click_on_site(site_account_number):
    xpath = './/td[contains(.,"%s")]' % site_account_number
    site_el = finder.find_element_by_xpath(xpath)
    site_el.click()


def click_edit_link_on_site_page():
    xpath = './/ul[@class="uk-navbar-nav"]/li/a[contains(., "Edit")]'
    edit_btn = finder.find_element_by_xpath(xpath)
    edit_btn.click()


def open_site_for_editing(site_account_number):
    home_navigator.go_to_home_page()
    click_on_site(site_account_number)
    click_edit_link_on_site_page()


def following_sites():
    xpath = '//*[@id="data_table"]/tbody/tr[1]'
    finder.find_visible_element_by_xpath(xpath)
