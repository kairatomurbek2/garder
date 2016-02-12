from django.utils import timezone
from django.conf import settings
from main.parameters import DemoTrialSessionKeys, Groups
from webapp.models import DemoTrial, Employee
from django.contrib.auth.models import User


class DaysDeltaCalculator(object):
    @staticmethod
    def get_days_delta(date_obj):
        delta_between_today_and_given_date = date_obj - timezone.now()
        delta_in_days = delta_between_today_and_given_date.days + 1
        return delta_in_days


class DemoTrialCreator(object):
    employee = None

    def create_demo_trial_for_user(self):
        start_date = timezone.now()
        end_date = start_date + timezone.timedelta(days=settings.DEMO_TRIAL_DAYS)
        demo_trial = DemoTrial.objects.create(employee=self.employee, start_date=start_date,
                                              end_date=end_date)
        return demo_trial


class DemoTrialBlockHelper(object):
    @staticmethod
    def block(pws):
        pws.is_active = False
        pws.save()

    @staticmethod
    def unblock(pws, request):
        pws.is_active = True
        pws.save()
        pws_employees = Employee.objects.filter(pws=pws)
        for employee in pws_employees:
            employee.has_paid = True
            employee.save()
        DemoTrialBlockHelper._remove_demo_trial_kyes_from_session(request)

    @staticmethod
    def _remove_demo_trial_kyes_from_session(request):
        request.session.pop(DemoTrialSessionKeys.demo_days_left_key, None)
        request.session.pop(DemoTrialSessionKeys.demo_days_left_message_key, None)


class PayAndActivate(object):
    @staticmethod
    def pay_and_activate(pws, request):
        DemoTrialBlockHelper.unblock(pws, request)


class DemoTrialPeriodNotSetError(Exception):
    pass


class DemoTrialPeriodExpiredError(Exception):
    pass


class TrialPeriodChecker(object):
    employee = None
    demo_days_left = None

    def execute(self):
        if not self.employee.has_paid:
            employee_demo_trials = list(self.employee.demo_trials.all())
            if len(employee_demo_trials) == 0:
                raise DemoTrialPeriodNotSetError()
            else:
                max_end_date = max([d.end_date for d in employee_demo_trials])
                self.demo_days_left = DaysDeltaCalculator.get_days_delta(max_end_date)
                if self.demo_days_left <= 0:
                    pws_list = list(self.employee.pws.all())
                    for pws in pws_list:
                        if pws.is_active:
                            DemoTrialBlockHelper.block(pws)
                    raise DemoTrialPeriodExpiredError()


class IsEmployeeInTrialPeriod(object):
    @staticmethod
    def check(user):
        """

        :type user: User
        :return:
        """
        if user.is_superuser or user.groups.filter(name=Groups.ad_auth) or user.groups.filter(name=Groups.superadmin):
            return False
        if user.groups.filter(name=Groups.pws_owner).count():  # this is pws owner and did not pay
            if not user.employee.has_paid:
                return True
            return False
        else:
            pws = user.employee.get_pws_list()[0]
            owner = pws.employees.filter(user__groups__name=Groups.pws_owner)[0]
            if not owner.has_paid:
                return True
        return False
