BASE_URL = 'http://127.0.0.1:8000'


def get_url(url):
    return BASE_URL + url


URLS = {
    'home': '/',
    'site_list': '/',
    'login': '/accounts/login/',
    'site_detail': '/site/%s/',
    'pws_list': '/pws/',
    'pws_add': '/pws/add/',
    'pws_edit': '/pws/edit/%s/',
}

LOGINS = {
    'root': {
        'username': 'root',
        'password': '1qaz@WSX'
    },
    'admin': {
        'username': 'admin',
        'password': 'admin'
    },
    'surveyor': {
        'username': 'surveyor',
        'password': 'surveyor',
    },
    'tester': {
        'username': 'tester',
        'password': 'tester'
    }
}


class Xpath:
    forms = {
        'auth': '//form[@name="auth"]',
        'site_filter': '//form[@name="site_filter"]',
        'pws': '//form[@name="pws"]',
    }

    text_fields = {
        'auth_username': '//input[@name="username"]',
        'auth_password': '//input[@name="password"]',
        'city': '//input[@name="city"]',
        'address1': '//input[@name="address1"]',
        'customer': '//input[@name="customer"]',
        'pws': '//input[@name="pws"]',
        'site_use': '//input[@name="site_use"]',
        'site_type': '//input[@name="site_type"]',
        'number': '//input[@name="number"]',
        'name': '//input[@name="name"]',
        'notes': '//textarea[@name="notes"]',
    }

    selects = {
        'water_source': '//select[@name="water_source"]',
    }

    checkboxes = {

    }

    radiobuttons = {

    }

    buttons = {
        'auth_submit': '//input[@type="submit"]'
    }

    links = {

    }