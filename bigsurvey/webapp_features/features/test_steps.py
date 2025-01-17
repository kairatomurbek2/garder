from lettuce import step

from data import get_url, Urls
from main.parameters import Messages
from webapp import models


@step('I directly open "test_add" page for hazard with pk "(\d+)"')
def directly_open_test_add_page(step, hazard_pk):
    step.given('I open "%s"' % get_url(Urls.test_add % hazard_pk))


@step('I directly open "test_detail" page with pk "(\d+)"')
def directly_open_test_detail_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.test_detail % pk))


@step('I open "test_list" page')
def open_test_list_page(step):
    step.given('I click "tests" menu link')


@step('I open "test_detail" page with pk "(\d+)"')
def open_test_detail_page(step, pk):
    step.given('I open "test_list" page')
    step.given('I click "test_%s_detail" link' % pk)


@step('I open "test_add" page for hazard with pk "(\d+)"')
def open_test_add_page(step, hazard_pk):
    step.given('I open "hazard_detail" page with pk "%s"' % hazard_pk)
    step.given('I click "hazard_%s_test_add" link' % hazard_pk)


@step('I directly open "test_edit" page with pk "(\d+)"')
def directly_open_test_edit_page(step, pk):
    step.given('I open "%s"' % get_url(Urls.test_edit % pk))


@step('I open "test_edit" page with pk "(\d+)"')
def open_test_edit_page(step, pk):
    hazard = models.Test.objects.get(pk=pk).bp_device
    step.given('I open "hazard_detail" page with pk "%s"' % hazard.pk)
    step.given('I click "test_%s_edit" link' % pk)


@step('I should be at "test_add" page for hazard with pk "(\d+)"')
def check_test_add_page(step, hazard_pk):
    step.given('I should be at "%s"' % get_url(Urls.test_add % hazard_pk))


@step('I should be at "test_edit" page with pk "(\d+)"')
def check_test_edit_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.test_edit % pk))


@step('I should see "test adding success" message')
def check_test_adding_success_message(step):
    step.given('I should see "%s"' % Messages.Test.adding_success)


@step('I should see "test adding error" message')
def check_test_adding_error_message(step):
    step.given('I should see "%s"' % Messages.Test.adding_error)


@step('I should see "test editing success" message')
def check_test_editing_success_message(step):
    step.given('I should see "%s"' % Messages.Test.editing_success)


@step('I should see "test editing error" message')
def check_test_editing_error_message(step):
    step.given('I should see "%s"' % Messages.Test.editing_error)


@step('I should be at "test_detail" page with pk "(\d+)"')
def check_test_detail_page(step, pk):
    step.given('I should be at "%s"' % get_url(Urls.test_detail % pk))


@step('Hazard with pk "(\d+)" has "(Air Gap|AVB|DC|DCDA|RP|RPDA|PVB|SVB|HBVB)" assembly type')
def set_hazard_assembly_type(step, pk, assembly_type):
    bp_device = models.BPDevice.objects.get(pk=pk)
    bp_device.bp_type_present = assembly_type
    bp_device.save()


@step('I directly open "test_list" page')
def open_test_list(step):
    step.given('I open "%s"' % get_url(Urls.test_list))
