from django.core.urlresolvers import resolve
from django.shortcuts import redirect
from main.parameters import DemoTrialMessages, DemoTrialSessionKeys, Groups
from webapp.actions.demo_trial import TrialPeriodChecker, \
    DemoTrialPeriodNotSetError, DemoTrialPeriodExpiredError


class DemoTrialWatchDog(object):
    def process_request(self, request):
        user = request.user
        try:
            pws = user.employee.get_pws_list()
        except AttributeError:
            return
        for pws_item in pws:
            if not self.excluded_pages(request):
                employee = pws_item.employees.filter(user__groups__name=Groups.pws_owner)[0]
                try:
                    checker = TrialPeriodChecker()
                    checker.employee = employee
                    checker.execute()
                    demo_days_left = checker.demo_days_left
                    if demo_days_left:
                        request.session[DemoTrialSessionKeys.demo_days_left_key] = demo_days_left
                        request.session[DemoTrialSessionKeys.demo_days_left_message_key] = DemoTrialMessages.demo_days_left_info % demo_days_left
                except DemoTrialPeriodNotSetError:
                    request.session['demo_trial_error'] = 'No end date provided to employee %s' % employee
                except DemoTrialPeriodExpiredError:
                    return redirect('webapp:activate_blocked_pws')

    @staticmethod
    def excluded_pages(request):
        exceptional_pages = [
            'activate_blocked_pws',
            'accounts:login',
            'logout',
            'password_reset',
            'password_reset_done',
            'password_reset_activation',
            'password_reset_complete',
            'pws_owner_registration',
            'demo_trial_paypal'
        ]
        name = resolve(request.path).url_name
        if name in exceptional_pages:
            return True
        else:
            return False
