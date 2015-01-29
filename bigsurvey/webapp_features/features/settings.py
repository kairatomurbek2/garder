BASE_URL = 'http://127.0.0.1:8000'


def get_url(url):
    return BASE_URL + url


class URLs:
    home = "/"
    login = '/accounts/login/'
    site_list = '/'
    site_detail = '/site/%s/'
    site_add = '/site/add/'
    site_edit = '/site/edit/'
    pws_list = '/pws/'
    pws_add = '/pws/add/'
    pws_edit = '/pws/edit/%s/'
    customer_list = '/customer/'
    customer_detail = '/customer/%s/'
    customer_add = '/customer/add/'
    customer_edit = '/customer/edit/%s'


class Logins:
    root = {
        'username': 'root',
        'password': '1qaz@WSX'
    }
    admin = {
        'username': 'admin',
        'password': 'admin'
    }
    surveyor = {
        'username': 'surveyor',
        'password': 'surveyor',
    }
    tester = {
        'username': 'tester',
        'password': 'tester'
    }


class Xpath:
    form_pattern = './/form[@name="%s"]'
    input_pattern = './/input[@name="%s"]'
    textarea_pattern = './/textarea[@nam="%s"]'
    select_pattern = './/select[@name="%s"]',
    option_pattern_by_value = './/option[@value="%s"]'
    option_pattern_by_exact_text = './/option[. = "%s"]'
    option_pattern_by_substr_text = './/option[contains(., "%s")]'
    checkbox_pattern_by_value = './/input[type="checkbox"][@value="%s"]'
    checkbox_pattern_by_exact_text = './/input[type="checkbox"][. = "%s"]'
    checkbox_pattern_by_substr_text = './/input[type="checkbox"][contains(., "%s")]'
    radiobutton_pattern_by_value = './/input[type="radio"][@value="%s"]'
    radiobutton_pattern_by_exact_text = './/'
    radiobutton_pattern_by_substr_text = './/radio[contains(., "%s")]'

    checkboxes = {

    }

    radiobuttons = {

    }

    buttons = {
        'auth_submit': '//input[@type="submit"]'
    }

    links = {

    }