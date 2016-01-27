from webapp.actions.sample_data import SampleSitesJsonUploader
from webapp.actions.sites import FilterSitesAction
from webapp.actions.users import AddUserAction


class UserManagementActionsBuilder(object):
    @staticmethod
    def get_user_add_action(user, user_form, employee_form, test_kit_form, cert_form):
        action = AddUserAction()
        action.user = user
        action.user_form = user_form
        action.employee_form = employee_form
        action.test_kit_form = test_kit_form
        action.cert_form = cert_form
        return action


class SiteFilteringActionsBuilder(object):
    @staticmethod
    def get_sites_filtered(sites_filtering_form, pws_list, sites):
        action = FilterSitesAction()
        action.sites_filtering_form = sites_filtering_form
        action.pws_list = pws_list
        action.sites = sites
        return action


class SampleSitesJsonUploaderBuilder(object):
    @staticmethod
    def load_sample_data(pws):
        action = SampleSitesJsonUploader()
        action.pws = pws
        return action
