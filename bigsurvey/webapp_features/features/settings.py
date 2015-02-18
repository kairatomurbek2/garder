from main.parameters import Messages


BASE_URL = 'http://127.0.0.1:8000'


def get_url(url):
    return BASE_URL + url


class Urls:
    home = '/'
    login = '/accounts/login/'
    logout = '/accounts/logout/'
    site_list = '/'
    site_detail = '/site/%s/'
    site_add = '/site/add/'
    site_edit = '/site/%s/edit/'
    pws_list = '/pws/'
    pws_add = '/pws/add/'
    pws_edit = '/pws/%s/edit/'
    customer_list = '/customer/'
    customer_detail = '/customer/%s/'
    customer_add = '/customer/add/'
    customer_edit = '/customer/%s/edit/'
    survey_detail = '/survey/%s/'
    survey_edit = '/survey/%s/edit/'
    survey_add = '/site/%s/%s/addsurvey/'
    hazard_detail = '/hazard/%s/'
    hazard_add = '/survey/%s/addhazard/'
    hazard_edit = '/hazard/%s/edit/'
    test_add = '/hazard/%s/addtest/'
    test_edit = '/test/%s/edit/'
    user_list = '/user/'
    user_add = '/user/add/'
    user_edit = '/user/%s/edit/'


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
    non_existent_user = {
        'username': 'non_existent_username',
        'password': 'non_existent_password'
    }


class Xpath:
    class Pattern:
        # Common
        form = './/form[@name="%s"]'
        input = './/input[@name="%s"]'
        textarea = './/textarea[@name="%s"]'
        select = './/select[@name="%s"]'
        option_by_value = './/option[@value="%s"]'
        option_by_exact_text = './/option[. = "%s"]'
        option_by_substr = './/option[contains(., "%s")]'
        checkbox_by_value = './/input[type="checkbox"][@value="%s"]'
        checkbox_by_exact_text = './/input[type="checkbox"][. = "%s"]'
        checkbox_by_substr = './/input[type="checkbox"][contains(., "%s")]'
        radiobutton_by_value = './/input[type="radio"][@value="%s"]'
        radiobutton_by_exact_text = './/input[type="radio"][. = "%"]'
        radiobutton_by_substr = './/input[type="radio"][contains(., "%s")]'
        button = './/input[@type="button"]'
        submit_button = './/input[@type="submit"]'
        reset_button = './/input[@type="reset"]'
        button_with_text = './/button[contains(., "%s")]'

        # Specific
        text_inside_element = './/*[contains(., "%s")]'
        menu_link = './/a[@id="%s_link"]'
        site_service = './/div[@id="%s_content"]'
        validation_error_by_exact_text = './/../ul[@class="errorlist"]/li[. = "%s"]'
        validation_error_by_substr = './/../ul[@class="errorlist"]/li[contains(., "%s")]'
        customer_select_button = './/button[@data-id="%s"]'
        commit_dialog_button = './/a[@id="commit_site_menu_button"]'