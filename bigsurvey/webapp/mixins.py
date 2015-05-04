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
    def has_perm(request, obj):
        pass


class SiteObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_sites') or \
               request.user.has_perm('webapp.access_to_pws_sites') and obj.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_site_by_customer_account') and request.session['site_pk'] == obj.pk


class SurveyObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_surveys') or \
               request.user.has_perm('webapp.access_to_pws_surveys') and obj.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_surveys') and obj.surveyor == request.user and obj.site.pws == request.user.employee.pws


class HazardObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_hazards') or \
               request.user.has_perm('webapp.access_to_pws_hazards') and obj.site.pws == request.user.employee.pws


class TestObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_tests') or \
               request.user.has_perm('webapp.access_to_pws_tests') and obj.bp_device.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_tests') and obj.tester == request.user and obj.bp_device.site.pws == request.user.employee.pws


class UserObjectMixin(ObjectMixin):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_users') or \
               request.user.has_perm('webapp.access_to_pws_users') and obj.employee.pws == request.user.employee.pws