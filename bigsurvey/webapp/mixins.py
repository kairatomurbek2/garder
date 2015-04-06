from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from abc import ABCMeta, abstractmethod
import models


class PermissionRequiredMixin(View):
    permission = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        if self.permission and not self.request.user.has_perm(self.permission):
            raise Http404
        return super(PermissionRequiredMixin, self).dispatch(*args, **kwargs)


class ObjectMixin(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def has_perm(user, obj):
        pass


class SiteObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(user, obj):
        return user.has_perm('webapp.access_to_all_sites') or \
               user.has_perm('webapp.access_to_pws_sites') and obj.pws == user.employee.pws


class SurveyObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(user, obj):
        return user.has_perm('webapp.access_to_all_surveys') or \
               user.has_perm('webapp.access_to_pws_surveys') and obj.site.pws == user.employee.pws or \
               user.has_perm('webapp.access_to_own_surveys') and obj.surveyor == user


class HazardObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(user, obj):
        return user.has_perm('webapp.access_to_all_hazards') or \
               user.has_perm('webapp.access_to_pws_hazards') and obj.site.pws == user.employee.pws


class TestObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(user, obj):
        return user.has_perm('webapp.access_to_all_tests') or \
               user.has_perm('webapp.access_to_pws_tests') and obj.bp_device.survey.site.pws == user.employee.pws or \
               user.has_perm('webapp.access_to_own_tests') and obj.tester == user


class UserObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(user, obj):
        return user.has_perm('webapp.access_to_all_users') or \
               user.has_perm('webapp.access_to_pws_users') and obj.employee.pws == user.employee.pws