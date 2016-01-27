import os
import helper
from datetime import datetime

from django.conf import settings

from django.core.files import File
from lettuce import step

from main.parameters import Messages

from webapp import models
from webapp_features.features.data import get_url, Xpath
from webapp_features.features.data import Urls


@step('I directly open "pws_list" page')
def directly_open_pws_list_page(step):
    step.given('I open "%s"' % get_url(Urls.pws_list))


@step('I open "pws_list" page')
def open_pws_list_page(step):
    step.given('I open "home" page')
    step.given('I click "pws" menu link')


@step('I directly open "pws_add" page')
def directly_open_pws_add_page(step):
    step.given('I open "%s"' % get_url(Urls.pws_add))


@step('I directly open "pws_detail" page with pk "(\d+)"')
def directly_open_pws_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.pws_detail % pk))


@step('I open "pws_detail" page with pk "(\d+)"')
def open_pws_detail_page(step, pk):
    step.given('I open "pws_list" page')
    step.given('I click "pws_%s_detail" link' % pk)


@step('I directly open "snapshot" page with pk (\d+)')
def directly_open_snapshot_page(step, pws_pk):
    step.given('I open "%s"' % get_url(Urls.pws_snapshot % pws_pk))


@step('I open "snapshot" page with pk (\d+)')
def open_snapshot_page(step, pws_pk):
    step.given('I open "pws_list" page')
    step.given('I click "pws_%s_snapshot" link' % pws_pk)


@step('I open "pws_add" page')
def open_pws_add_page(step):
    step.given('I open "pws_list" page')
    step.given('I click "pws_add" link')


@step('I directly open "pws_edit" page with pk "(\d+)"')
def directly_open_pws_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.pws_edit % pk))


@step('I open "pws_edit" page with pk "(\d+)"')
def open_pws_edit_page(step, pk):
    step.given('I open "pws_detail" page with pk "%s"' % pk)
    step.given('I click "pws_%s_edit" link' % pk)


@step('I should be at "pws_list" page')
def check_pws_add_page(step):
    step.given('I should be at "%s"' % get_url(Urls.pws_list))


@step('I should be at "pws_add" page')
def check_pws_add_page(step):
    step.then('I should be at "%s"' % get_url(Urls.pws_add))


@step('I should be at "pws_detail" page with pk "(\d+)"')
def check_pws_detail_page(step, pk):
    step.then('I should be at "%s"' % get_url(Urls.pws_detail % pk))


@step('I should be at "pws_edit" page with pk "(\d+)"')
def check_pws_edit_page(step, pk):
    step.then('I should be at "%s"' % get_url(Urls.pws_edit % pk))


@step('I should see "pws adding success" message')
def check_pws_adding_success_message(step):
    step.then('I should see "%s"' % Messages.PWS.adding_success)


@step('I should see "pws adding error" message')
def check_pws_adding_error_message(step):
    step.then('I should see "%s"' % Messages.PWS.adding_error)


@step('I should see "pws editing success" message')
def check_pws_editing_success_message(step):
    step.given('I should see "%s"' % Messages.PWS.editing_success)


@step('I should see "pws editing error" message')
def check_pws_editing_error_message(step):
    step.given('I should see "%s"' % Messages.PWS.editing_error)


@step('New letter types were created for PWS with number "(.*)"')
def check_new_lettertypes_were_created(step, number):
    pws = models.PWS.objects.get(number=number)
    assert pws.letter_types.exists(), 'PWS has no Letter Types'


@step('"(.*)" should be uploaded')
def check_pws_logo_upload(step, file):
    logo = os.path.join(settings.PWS_LOGOS_DIR, file)
    assert os.path.isfile(logo), 'There is no logo'


@step('"(.*)" should be deleted')
def clear_logo(step, file):
    logo = os.path.join(settings.PWS_LOGOS_DIR, file)
    assert not os.path.isfile(logo), 'File was not deleted'


@step('PWS with pk "(\d+)" has uploaded logo')
def add_pws_logo(step, pk):
    pws = models.PWS.objects.get(pk=pk)
    pws.logo.save('pws-6-logo.jpg', File(open(os.path.join(settings.STUB_FILES_DIR, 'logo.jpg'))))


@step('PWS with pk "(\d+)" should contain "(.*)" in "(.*)" field')
def check_pws_field_value(step, pk, value, field):
    pws = models.PWS.objects.get(pk=pk)
    actual_value = getattr(pws, field)
    assert value == actual_value, 'Expected "%s" in "%s" field, found "%s"' % (value, field, actual_value)


@step('PWS with pk (\d+) has at least one site')
def create_site_for_pws(step, pws_pk):
    pws = models.PWS.objects.get(pk=pws_pk)
    cust_code = models.CustomerCode.objects.get(pk=3)
    if not pws.sites.all().exists():
        models.Site.objects.create(
            pws=pws,
            cust_number="temp1",
            city="city1",
            address1="address1",
            cust_name="cust1",
            cust_code=cust_code
        )


@step('PWS with pk (\d+) has (\d+) hazard\(s\)')
def create_hazards_for_pws(step, pws_pk, number):
    pws = models.PWS.objects.get(pk=pws_pk)
    site = pws.sites.all().first()
    service_type = models.ServiceType.objects.get(pk=3)
    hazard_type = models.HazardType.objects.get(pk=1)
    i = 0
    while i < int(number):
        models.Hazard.objects.create(site=site, service_type=service_type, hazard_type=hazard_type)
        i += 1


@step('PWS with pk (\d+) has (\d+) survey\(s\)')
def create_surveys_for_pws(step, pws_pk, number):
    pws = models.PWS.objects.get(pk=pws_pk)
    site = pws.sites.all().first()
    service_type = models.ServiceType.objects.get(pk=3)
    i = 0
    while i < int(number):
        models.Survey.objects.create(survey_date=datetime.now().date(), service_type=service_type, site=site)
        i += 1


@step('PWS with pk (\d+) has (\d+) bp-device\(s\) of type "([a-zA-Z ]+)" installed (At Meter|Internal)')
def create_devices_for_pws(step, pws_pk, number, bp_type, location):
    pws = models.PWS.objects.get(pk=pws_pk)
    site = pws.sites.all().first()
    service_type = models.ServiceType.objects.get(pk=3)
    hazard_type = models.HazardType.objects.get(pk=1)
    assembly_location = models.AssemblyLocation.objects.get(assembly_location=location)
    i = 0
    while i < int(number):
        bp_device = models.BPDevice.objects.create(bp_type_present=bp_type, assembly_location=assembly_location)
        models.Hazard.objects.create(site=site, service_type=service_type, hazard_type=hazard_type, bp_device=bp_device)
        i += 1


@step('PWS with pk (\d+) has (\d+) letter\(s\) of type "([a-zA-Z ]+)"')
def create_letters_for_pws(step, pws_pk, number, type):
    pws = models.PWS.objects.get(pk=pws_pk)
    site = pws.sites.all().first()
    hazard = site.hazards.all().first()
    letter_type = models.LetterType.objects.get(letter_type=type, pws=pws)
    i = 0
    while i < int(number):
        models.Letter.objects.create(letter_type=letter_type, hazard=hazard, site=site, already_sent=True)
        i += 1


@step('I should see values in order "([0-9,]+)"')
def see_snapshot_values(step, values_string):
    values = values_string.split(",")
    page_values = helper.find_multiple(Xpath.Pattern.snapshot_values)
    i = 0
    result = True
    for item in values:
        if int(item) != int(page_values[i].text):
            result = False
            break
        i += 1
    assert result
