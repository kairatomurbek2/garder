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
               request.user.has_perm('webapp.access_to_pws_sites') and obj.pws in request.user.employee.pws.all() or \
               request.user.has_perm('webapp.access_to_site_by_customer_account') and request.session['site_pk'] == obj.pk


class SurveyPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_surveys') or \
               request.user.has_perm('webapp.access_to_pws_surveys') and obj.site.pws in request.user.employee.pws.all() or \
               request.user.has_perm('webapp.access_to_own_surveys') and obj.surveyor == request.user and obj.site.pws in request.user.employee.pws.all()


class HazardPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_hazards') or \
               request.user.has_perm('webapp.access_to_pws_hazards') and obj.site.pws in request.user.employee.pws.all() or \
               obj.tests.filter(tester=request.user).exists()


class TestPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_tests') or \
               request.user.has_perm('webapp.access_to_pws_tests') and obj.bp_device.site.pws in request.user.employee.pws.all() or \
               request.user.has_perm('webapp.access_to_own_tests') and obj.tester == request.user


class UserPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_users') or \
               request.user.has_perm('webapp.access_to_pws_users') and \
               set(obj.employee.pws.all()).issubset(request.user.employee.pws.all()) or \
               request.user.has_perm('webapp.access_to_multiple_pws_users') and \
               set(obj.employee.pws.all()).issubset(request.user.employee.pws.all())


class LetterPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.full_letter_access') or \
               request.user.has_perm('webapp.pws_letter_access') and obj.site.pws in request.user.employee.pws.all()


class LetterTypePermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_lettertypes') or \
               request.user.has_perm('webapp.access_to_pws_lettertypes') and obj.pws in request.user.employee.pws.all()


class ImportLogPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_import_logs') or \
               request.user.has_perm('webapp.access_to_pws_import_logs') and obj.pws in request.user.employee.pws.all()
