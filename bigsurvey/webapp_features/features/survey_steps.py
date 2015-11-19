from lettuce import step, world
from main.parameters import Messages
from webapp import models
from webapp_features.features import helper
from webapp_features.features.common_steps import click_element_by_xpath
from webapp_features.features.data import Xpath, get_url, Urls
from time import sleep


@step('I directly open "survey_detail" page with pk "(\d+)"')
def directly_open_survey_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.survey_detail % pk))


@step('I open "survey_detail" page with pk "(\d+)"')
def open_survey_detail_page(step, pk):
    site = models.Survey.objects.get(pk=pk).site
    step.given('I open "site_detail" page with pk "%s"' % site.pk)
    step.given('I click "survey_%s_detail" link' % pk)


@step('I directly open "survey_add" page for site with pk "(\d+)" and service "([a-z]+)"')
def directly_open_survey_add_page_for_site(step, site_pk, service_type):
    step.given('I open "%s"' % get_url(Urls.survey_add % (site_pk, service_type)))


@step('I open "survey_add" page for site with pk "(\d+)" and service "([a-z]+)"')
def open_survey_add_page_for_site(step, site_pk, service_type):
    step.given('I open "site_detail" page with pk "%s"' % site_pk)
    click_element_by_xpath(Xpath.site_surveys_button)
    step.given('I click "site_%s_service_%s_survey_add" link' % (site_pk, service_type))


@step('I directly open "survey_edit" page with pk "(\d+)"')
def directly_open_survey_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.survey_edit % pk))


@step('I open "survey_edit" page with pk "(\d+)"')
def open_survey_edit_page(step, pk):
    step.given('I open "survey_detail" page with pk "%s"' % pk)
    step.given('I click "survey_%s_edit" link' % pk)


@step('I should be at "survey_detail" page with pk "(\d+)"')
def check_survey_detail_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.survey_detail % pk))


@step('I should be at "survey_add" page for site with pk "(\d+)" and service "([a-z]+)"')
def check_survey_add_page(step, pk, service):
    step.given('I should be at "%s"' % get_url(Urls.survey_add % (pk, service)))


@step('I should be at "survey_edit" page with pk "(\d+)"')
def check_survey_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.survey_edit % pk))


@step('I should see "survey adding error" message')
def check_survey_adding_error_message(step):
    step.given('I should see "%s"' % Messages.Survey.adding_error)


@step('I should see "survey adding success" message')
def check_survey_adding_success_message(step):
    step.given('I should see "%s"' % Messages.Survey.adding_success)


@step('I should see "survey editing error" message')
def check_survey_editing_error_message(step):
    step.given('I should see "%s"' % Messages.Survey.editing_error)


@step('I should see "survey editing success" message')
def check_survey_editing_success_message(step):
    step.given('I should see "%s"' % Messages.Survey.editing_success)


@step('I close hazard modal')
def close_hazard_modal(step):
    hazard_modal = helper.find(Xpath.hazard_modal)
    helper.check_element_exists(hazard_modal, 'Hazard modal was not found')
    close_button = helper.find(Xpath.modal_close_button, hazard_modal)
    close_button.click()


@step('Marker should be at "(.*)" latitude and "(.*)" longitude')
def check_marker_position(step, latitude, longitude):
    map_latitude = world.browser.execute_script('return GoogleMap.marker.getPosition().lat()')
    map_longitude = world.browser.execute_script('return GoogleMap.marker.getPosition().lng()')
    assert int(latitude) == map_latitude, 'Latitude: expected "%s", got "%s"' % (latitude, map_latitude)
    assert int(longitude) == map_longitude, 'Longitude: expected "%s", got "%s"' % (longitude, map_longitude)


@step('Marker should be approximately inside Bishkek')
def check_market_in_kyrgyzstan(step):
    import time
    # Wait until GoogleMap is updating
    time.sleep(3)
    latitude = 42.8, 42.9
    longitude = 74.5, 74.7
    map_latitude = world.browser.execute_script('return GoogleMap.marker.getPosition().lat()')
    map_longitude = world.browser.execute_script('return GoogleMap.marker.getPosition().lng()')
    assert latitude[0] <= map_latitude <= latitude[1], 'Latitude expected to be in range (%s, %s), got %s' % (latitude[0], latitude[1], map_latitude)
    assert longitude[0] <= map_longitude <= longitude[1], 'Longitude expected to be in range (%s, %s), got %s' % (longitude[0], longitude[1], map_longitude)


@step('Site with pk "(\d+)" has "(potable|fire|irrigation)" service turned (on|off)')
def set_service_type_present(step, pk, service_type, value):
    site = models.Site.objects.get(pk=pk)
    value = True if value == 'on' else False
    setattr(site, '%s_present' % service_type, value)
    site.save()


@step('Site with pk "(\d+)" should have "(potable|fire|irrigation)" service turned (on|off)')
def check_service_type_present(step, pk, service_type, value):
    sleep(1)
    site = models.Site.objects.get(pk=pk)
    value = True if value == 'on' else False
    site_value = getattr(site, '%s_present' % service_type)
    assert site_value == value, '%s service: expected %s, found %s' % (service_type.capitalize(), value, site_value)


@step('I directly open "survey_list" page')
def open_survey_list(step):
    step.given('I open "%s"' % get_url(Urls.survey_list))
