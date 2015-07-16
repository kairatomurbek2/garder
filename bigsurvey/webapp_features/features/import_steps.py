from lettuce import step
from main.parameters import Messages

from webapp_features.features import helper
from webapp_features.features.data import get_url, Urls, import_mappings, Xpath, DELIMITER


@step('I directly open "import" page')
def directly_open_import_page(step):
    step.given('I open "%s"' % get_url(Urls.import_page))


@step('I open "import" page')
def open_import_list_page(step):
    step.given('I open "home" page')
    step.given('I click "import" menu link')


@step('I open "import_log_list" page')
def open_import_log_list_page(step):
    step.given('I open "home" page')
    step.given('I click "import_log" menu link')


@step('I should be at "import_mappings" page')
def check_import_mappings_page(step):
    step.given('I should be at "%s"' % get_url(Urls.import_mappings))


@step('I should be at "import_mappings_process" page')
def check_import_mappings_page(step):
    step.given('I should be at "%s"' % get_url(Urls.import_mappings_process))


@step('I fill in mappings')
def fill_in_mappings(step):
    for model_field, value in import_mappings.items():
        select = helper.find(Xpath.Pattern.select_by_model_field % model_field)
        option = helper.find(Xpath.Pattern.option_by_value % value, select)
        option.click()


@step('I should see "required fields not filled" message')
def check_import_was_started_message(step):
    step.given('I should see "%s"' % Messages.Import.required_fields_not_filled)


@step('I should see "incorrect date format" message with params "(.*)"')
def check_incorrect_date_format_message(step, params):
    params = tuple(params.split(DELIMITER))
    text = Messages.Import.incorrect_date_format % params
    helper.check_text_exists_inside_element(Xpath.import_mappings_form_errors, text, '"%s" is not on page.' % text)


@step('I should see "duplicate cust numbers" message with params "(.*)"')
def check_incorrect_date_format_message(step, params):
    params = tuple(params.split(DELIMITER))
    text = Messages.Import.duplicate_cust_numbers % params
    helper.check_text_exists_inside_element(Xpath.import_mappings_form_errors, text, '"%s" is not on page.' % text)


@step('I should see "foreign key error" message with params "(.*)"')
def check_incorrect_date_format_message(step, params):
    params = tuple(params.split(DELIMITER))
    text = Messages.Import.foreign_key_error % params
    helper.check_text_exists_inside_element(Xpath.import_mappings_form_errors, text, '"%s" is not on page.' % text)


@step('I should see "required value is empty" message with params "(.*)"')
def check_incorrect_date_format_message(step, params):
    params = tuple(params.split(DELIMITER))
    text = Messages.Import.required_value_is_empty % params
    helper.check_text_exists_inside_element(Xpath.import_mappings_form_errors, text, '"%s" is not on page.' % text)


@step('Last import should have following data')
def check_import_sites_count(step):
    import_table = helper.find(Xpath.Pattern.table % 'import_logs')
    last_import_row = helper.find(Xpath.Pattern.table_row_by_number % 1, import_table)
    data = step.hashes[0]
    added_sites = helper.find(Xpath.import_row_sites_count % 'added_sites', last_import_row).text
    updated_sites = helper.find(Xpath.import_row_sites_count % 'updated_sites', last_import_row).text
    deactivated_sites = helper.find(Xpath.import_row_sites_count % 'deactivated_sites', last_import_row).text
    assert data['added_sites'] == added_sites, 'Expected %s added sites, found %s' % (data['added_sites'], added_sites)
    assert data['updated_sites'] == updated_sites, 'Expected %s updated sites, found %s' % (data['updated_sites'], updated_sites)
    assert data['deactivated_sites'] == deactivated_sites, 'Expected %s deactivated sites, found %s' % (data['deactivated_sites'], deactivated_sites)