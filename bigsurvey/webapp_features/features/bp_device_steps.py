from lettuce import step
from webapp.models import Hazard, User
from data import Urls, get_url


@step('Hazard with pk "(\d+)" has no bp device installed')
def uninstall_bp_device(step, hazard_pk):
    hazard = Hazard.objects.get(pk=hazard_pk)
    hazard.assembly_status = None
    hazard.bp_device = None
    hazard.save()


@step('Tester has no licence')
def remove_tester_licence(step):
    tester = User.objects.get(username="tester")
    tester.employee.has_licence_for_installation = False
    tester.employee.save()


@step('I directly open "bp_device_add" page for hazard with pk "(\d+)"')
def open_bp_device_add_page(step, hazard_pk):
    step.given('I open "%s"' % get_url(Urls.bp_device_add % hazard_pk))
