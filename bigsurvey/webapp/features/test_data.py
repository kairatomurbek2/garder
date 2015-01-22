BASE_URL = 'http://127.0.0.1:8000'


def get_url(url):
    return BASE_URL + url


class UiElements:
    class Xpath:
        text_fields = {
            'auth_username': "//input[@name='username']",
            'auth_password': "//input[@name='password']",
            'city': "//input[@name='city']",
            'address1': "//input[@name='address1']",
            'customer': "//input[@name='customer']",
            'pws': "//input[@name='pws']",
            'site_use': "//input[@name='site_use']",
            'site_type': "//input[@name='site_type']",
        }

        buttons = {
            'auth_submit': "//input[@type='submit']"
        }

        forms = {
            'auth': "//form[@name='auth']",
            'site_filter': "//form[@name='site_filter']"
        }

    links = {
        'home': {'url': '/'},
        'login': {'url': '/accounts/login/'},
        'site_list': {'url': '/'},
        'site_detail': {'url': '/site/%s/'},
        'pws_list': {'url': '/pws/'},
        'pws_add': {'url': '/pws/add/'},
        'pws_edit': {'url': '/pws/edit/%s/'},
    }


class TestData:
    logins = {
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