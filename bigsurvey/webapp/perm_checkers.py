from abc import ABCMeta, abstractmethod

class ObjectPermChecker(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def has_perm(request, obj):
        pass


class SitePermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_sites') or \
               request.user.has_perm('webapp.access_to_pws_sites') and obj.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_site_by_customer_account') and request.session['site_pk'] == obj.pk


class SurveyPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_surveys') or \
               request.user.has_perm('webapp.access_to_pws_surveys') and obj.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_surveys') and obj.surveyor == request.user and obj.site.pws == request.user.employee.pws


class HazardPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_hazards') or \
               request.user.has_perm('webapp.access_to_pws_hazards') and obj.site.pws == request.user.employee.pws or \
               obj.tests.filter(tester=request.user).exists()


class TestPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_tests') or \
               request.user.has_perm('webapp.access_to_pws_tests') and obj.bp_device.site.pws == request.user.employee.pws or \
               request.user.has_perm('webapp.access_to_own_tests') and obj.tester == request.user


class UserPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_users') or \
               request.user.has_perm('webapp.access_to_pws_users') and obj.employee.pws == request.user.employee.pws


class LetterPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        a = request.user.has_perm('webapp.full_letter_access') or \
            request.user.has_perm('webapp.pws_letter_access') and obj.site.pws == request.user.employee.pws
        return a