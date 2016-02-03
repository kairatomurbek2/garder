from django.core.urlresolvers import resolve
from django.shortcuts import redirect
from main.parameters import DemoTrialMessages, DemoTrialSessionKeys
from webapp.actions.demo_trial import TrialPeriodChecker, \
    DemoTrialPeriodNotSetError, DemoTrialPeriodExpiredError


class DemoTrialWatchDog(object):
    def process_request(self, request):
        if not self.excluded_pages(request):
            try:
                employee = request.user.employee
            except AttributeError:
                return
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
            'accounts:logout',
            'password_reset',
            'password_reset_done',
            'password_reset_activation',
            'password_reset_complete',
            'pws_owner_registration',
        ]
        name = resolve(request.path).url_name
        if name in exceptional_pages:
            return True
        else:
            return False
