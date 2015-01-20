BASE_URL = 'http://127.0.0.1:8000'


def get_url(url):
    return BASE_URL + url


class UiElements:
    class Xpath:
        text_fields = {
            'auth_username': "//input[@name='username']",
            'auth_password': "//input[@name='password']"
        }

        buttons = {
            'auth_submit': "//input[@type='submit']"
        }

    links = {
        'home': {'url': '/'},
        'login': {'url': '/accounts/login/'}
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