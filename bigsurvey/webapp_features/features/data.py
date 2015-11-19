from django.conf import settings

DELIMITER = ' :: '


def get_url(url):
    return settings.HOST + url


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
    pws_detail = '/pws/%s/'
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
    test_detail = '/test/%s/'
    unpaid_test_list = '/unsaved-tests/'
    user_list = '/user/'
    user_detail = '/user/%s/'
    user_add = '/user/add/'
    user_edit = '/user/%s/edit/'
    batch_update = '/batch_update/'
    letter_list = '/letter/'
    letter_detail = '/letter/%s/'
    letter_edit = '/letter/%s/edit/'
    letter_add = '/site/%s/add-letter/'
    letter_pdf = '/letter/%s/pdf/'
    import_page = '/import/'
    import_mappings = '/import-mappings/'
    import_mappings_process = '/import-mappings-process/'
    import_log_sites = '/import-log/%s/%s/'
    letter_type_edit = '/letter_type/%s/edit/'
    letter_type_list = '/letter_type/'
    tester_invite = '/tester-search/'
    kit_add = '/user/%s/kit-add/'
    kit_edit = '/kit-edit/%s/'
    cert_add = '/user/%s/cert-add/'
    cert_edit = '/cert-edit/%s/'
    survey_list = '/survey/'
    hazard_list = '/hazard/'
    tester_list = '/testers/'
    test_list = '/test/'


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
    pws_owner = {
        'username': 'owner',
        'password': 'admin'
    }
    non_existent_user = {
        'username': 'non_existent_username',
        'password': 'non_existent_password'
    }
    adauth = {
        'username': 'adauth',
        'password': 'adauth'
    }


class Xpath:
    class Pattern:
        # Common
        form = './/form[@name="%s"]'
        form_by_id = './/form[@id="%s"]'
        table = './/table[@id="%s"]'
        input = './/input[@name="%s"]'
        file_input = './/input[@type="file"][@name="%s"]'
        textarea = './/textarea[@name="%s"]'
        select = './/select[@name="%s"]'
        option_by_value = './/option[@value="%s"]'
        option_by_exact_text = './/option[. = "%s"]'
        option_by_substr = './/option[contains(., "%s")]'
        checkbox_by_value = './/input[@type="checkbox"][@name="%s"][@value="%s"]'
        checkbox_by_name = './/input[@type="checkbox"][@name="%s"]'
        radiobutton_by_value = './/input[@type="radio"][@name="%s"][@value="%s"]'
        button = './/button[@name="%s"]'
        button_with_label = './/button[contains(., "%s")]'
        link = './/a[@id="%s_link"]'
        link_by_href = './/a[@href="%s"]'
        link_by_exact_text = './/a[. = "%s"]'
        link_by_substr = './/a[contains(., "%s")]'

        # Specific
        text_inside_element = './/*[contains(., "%s")]'
        table_row_by_number = './/tbody/tr[%d]'
        menu_item = './/a[@id="%s_menu_link"]'
        validation_error_by_exact_text = './/../ul[@class="errorlist"]/li[. = "%s"]'
        validation_error_by_substr = './/../ul[@class="errorlist"]/li[contains(., "%s")]'
        pagination_link = './/a[@data-action="pagination"][@data-id="%s"]'
        site_detail_link = './/tr[@class="clickable-row"][@data-id="%s"]'
        excel_field_select_by_model_field = './/input[@value="%s"]/../following-sibling::td/select'
        site_id = './/tr/td[1][text()="%s"]'
        site_table_text = './/tbody//td[contains(., "%s")]'

    class Paypal:
        username = './/input[@name="login_email"]'
        password = './/input[@name="login_password"]'
        submit_button = './/input[@name="login.x"]'
        login_button = './/input[@name="login_button"]'
        continue_button = './/input[@name="continue"]'

    form_element = './/input|.//textarea|.//select'
    csrfmiddlewaretoken = './/input[@name="csrfmiddlewaretoken"]'
    top_menu = './/ul[@data-content="menu"]'
    canvas_menu = './/ul[@data-content="canvas-menu"]'
    more_link = './/li[@id="bfp_menu"]/a'
    import_mappings_form_errors = './/div[contains(@class, "uk-alert-danger")]/ul/li'
    hazard_modal = './/div[@id="hazard-form-modal"]'
    pay_modal = './/div[@id="pay-modal"]'
    payment_step_2 = './/div[@data-content="step-2"]'
    modal_close_button = './/a[contains(@class, "uk-modal-close")]'
    import_row_sites_count = './/td[@data-content="%s"]/a'
    site_hazards_button = '//a[@id="hazards_button"]'
    site_surveys_button = '//a[@id="surveys_button"]'


import_mappings = {
    "cust_city": 18,
    "city": 8,
    "cust_code": 2,
    "zip": 10,
    "street_number": 5,
    "meter_number": 12,
    "connect_date": 3,
    "route": 11,
    "meter_size": 13,
    "cust_number": 0,
    "apt": 7,
    "cust_zip": 20,
    "state": 9,
    "meter_reading": 14,
    "address1": 6,
    "cust_address1": 16,
    "cust_name": 15,
    "cust_state": 19,
    "cust_address2": 17,
    "next_survey_date": 4
}


class PaypalCredentials:
    username = 'bigsurvey@test.com'
    password = '1qaz@WSX'
