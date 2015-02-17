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
        if self.permission:
            if not self.request.user.has_perm(self.permission):
                raise Http404
        return super(PermissionRequiredMixin, self).dispatch(*args, **kwargs)


class ObjectMixin(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def has_perm(request, obj):
        pass


class SiteObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_sites') or \
               request.user.has_perm('webapp.access_to_pws_sites') and obj.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_survey_sites') and obj.inspections.filter(
                   assigned_to=request.user) or \
               request.user.has_perm('webapp.access_to_test_sites') and obj.test_perms.filter(given_to=request.user)


class SurveyObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        if request.user.has_perm('webapp.access_to_all_surveys') or \
                        request.user.has_perm('webapp.access_to_pws_surveys') and obj.site.pws == request.user.employee.pws:
            return True
        if request.user.has_perm('webapp.access_to_own_surveys'):
            inspections = models.Inspection.objects.filter(assigned_to=request.user,
                                                           is_active=True,
                                                           site=obj.site)
            try:
                if inspections[0]:
                    return True
            except IndexError:
                return False
        return False


class HazardObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_hazards') or \
               request.user.has_perm('webapp.access_to_pws_hazards') and obj.survey.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_hazards') and models.Inspection.objects.filter(
                   site=obj.survey.site, assigned_to=request.user, is_active=True) or \
               request.user.has_perm('webapp.access_to_site_hazards') and models.TestPermission.objects.filter(
                   site=obj.survey.site, given_to=request.user, is_active=True)


class TestObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_tests') or \
               request.user.has_perm('webapp.access_to_pws_tests') and obj.bp_device.survey.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_tests') and obj.tester == request.user


class InspectionObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_inspections') or \
               request.user.has_perm('webapp.access_to_pws_inspections') and obj.site.pws == request.user.employee.pws


class UserObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_users') or \
               request.user.has_perm('webapp.access_to_pws_users') and obj.employee.pws == request.user.employee.pws