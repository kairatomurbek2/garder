from datetime import datetime
from lettuce import step, world
from main.parameters import Messages
from webapp import models
from webapp_features.features import helper
from webapp_features.features.data import Xpath, get_url, Urls


@step('I open "import_log_list" page')
def open_import_log_list_page(step):
    step.given('I open "home" page')
    step.given('I click "import_log" menu link')


@step('I should be at "import_log_list" page')
def check_import_log_list_page(step):
    step.given('I should be at "%s"' % get_url(Urls.import_log))


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


@step('The is performed import from "(.*)" by "(.*)" into "(.*)"')
def create_import(step, date, username, pws_number):
    user = models.User.objects.get(username=username)
    pws = models.PWS.objects.get(number=pws_number)
    import_log = models.ImportLog.objects.create(user=user, pws=pws)
    import_log.datetime = datetime.strptime(date, '%Y-%m-%d %H:%M')
    import_log.save()
    world.cache['import_log'] = import_log


@step('I open (added|updated|deactivated) sites of this import')
def open_sites_of_this_import(step, type):
    step.given('I open "%s"' % get_url(Urls.import_log_sites % (world.cache['import_log'].pk, type)))


@step('I should see added sites notification of this import')
def check_added_sites_notification(step):
    step.given('I should see "%s"' % Messages.Import.added_sites_header % world.cache['import_log'].datetime.strftime('%b. %d, %Y, %H:%M'))


@step('I should see updated sites notification of this import')
def check_added_sites_notification(step):
    step.given('I should see "%s"' % Messages.Import.updated_sites_header % world.cache['import_log'].datetime.strftime('%b. %d, %Y, %H:%M'))


@step('I should see deactivated sites notification of this import')
def check_added_sites_notification(step):
    step.given('I should see "%s"' % Messages.Import.deactivated_sites_header % world.cache['import_log'].datetime.strftime('%b. %d, %Y, %H:%M'))
