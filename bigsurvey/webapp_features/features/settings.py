from main.parameters import Messages


Messages = Messages

BASE_URL = 'http://127.0.0.1:8000'


def get_url(url):
    return BASE_URL + url


class Urls:
    home = '/'
    tester_home = '/tester-home/'
    login = '/accounts/login/'
    logout = '/accounts/logout/'
    site_list = '/'
    site_detail = '/site/%s/'
    site_add = '/site/add/'
    site_edit = '/site/%s/edit/'
    pws_list = '/pws/'
    pws_add = '/pws/add/'
    pws_edit = '/pws/%s/edit/'
    survey_detail = '/survey/%s/'
    survey_edit = '/survey/%s/edit/'
    survey_add = '/site/%s/%s/add-survey/'
    hazard_detail = '/hazard/%s/'
    hazard_add = '/site/%s/%s/add-hazard/'
    hazard_edit = '/hazard/%s/edit/'
    test_add = '/hazard/%s/add-test/'
    test_edit = '/test/%s/edit/'
    user_list = '/user/'
    user_add = '/user/add/'
    user_edit = '/user/%s/edit/'
    batch_update = '/batch_update/'
    letter_list = '/letter/'
    letter_detail = '/letter/%s/'
    letter_edit = '/letter/%s/edit/'
    letter_add = '/site/%s/add-letter/'
    letter_pdf = '/letter/%s/pdf/'


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
        checkbox_by_value = './/input[@type="checkbox"][@name="%s"][@value="%s"]'
        radiobutton_by_value = './/input[@type="radio"][@name="%s"][@value="%s"]'
        button = './/button[@name="%s"]'
        button_with_label = './/button[contains(., "%s")]'
        link_by_href = './/a[@href="%s"]'
        link_by_exact_text = './/a[. = "%s"]'
        link_by_substr = './/a[contains(., "%s")]'

        # Specific
        text_inside_element = './/*[contains(., "%s")]'
        menu_item = './/a[@id="%s_menu_link"]'
        site_service = './/div[@id="s%s_content"]'
        site_hazard_service = './/div[@id="h%s_content"]'
        validation_error_by_exact_text = './/../ul[@class="errorlist"]/li[. = "%s"]'
        validation_error_by_substr = './/../ul[@class="errorlist"]/li[contains(., "%s")]'
        customer_select_button = './/button[@data-id="%s"]'
        link = './/a[@id="%s_link"]'
        pagination_link = './/a[@data-action="pagination"][@data-id="%s"]'
        survey_detail = '//div[@id="spotable_content"]//table/tbody/tr[%s]//a'
        site_detail_link = './/tr[@class="clickable-row"][@data-id="%s"]'
        survey_edit_link = '//*[@class="uk-navbar-flip"]//a[1]'
        site_hazards_button = '//a[@id="hazards_button"]'
        site_surveys_button = '//a[@id="surveys_button"]'

    more_link = './/li[@id="bfp_menu"]/a'
    form_element = './/input|.//textarea|.//select'
    csrfmiddlewaretoken = './/input[@name="csrfmiddlewaretoken"]'