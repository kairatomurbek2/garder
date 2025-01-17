from abc import ABCMeta, abstractmethod
from webapp import models
from main.parameters import Groups


class ObjectPermChecker(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def has_perm(request, obj):
        pass


class SitePermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        site_pks = request.session.get('sites_pks')
        if not site_pks:
            site_pks = []
        return request.user.has_perm('webapp.access_to_all_sites') or \
               request.user.has_perm('webapp.access_to_pws_sites') and obj.pws in request.user.employee.pws.all() or \
               request.user.has_perm('webapp.access_to_site_by_customer_account') and obj.pk in site_pks


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
               request.user.has_perm('webapp.access_to_pws_hazards') and obj.site.pws in request.user.employee.pws.all()


class TestPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        return request.user.has_perm('webapp.access_to_all_tests') or \
               request.user.has_perm('webapp.access_to_pws_tests') and obj.bp_device.hazard.site.pws in request.user.employee.pws.all() or \
               obj.tester == request.user


class UserPermChecker(ObjectPermChecker):
    @staticmethod
    def has_perm(request, obj):
        perm = False
        testers_group = models.Group.objects.get(name=Groups.tester)
        super_admin_group = models.Group.objects.get(name=Groups.superadmin)
        if request.user.has_perm('webapp.access_to_all_users'):
            if request.user.has_perm('webapp.can_edit_super_admin'):
                perm = True
            else:
                perm = not(super_admin_group in obj.groups.all()) or obj == request.user
        elif request.user.has_perm('webapp.access_to_multiple_pws_users'):
            perm = set(obj.employee.pws.all()).issubset(request.user.employee.pws.all()) and obj.employee.pws.all() or \
                testers_group in obj.groups.all() and \
                bool(set(request.user.employee.pws.all()) & set(obj.employee.pws.all()))
        elif request.user.has_perm('webapp.access_to_pws_users'):
            perm = set(obj.employee.pws.all()).issubset(request.user.employee.pws.all()) and obj.employee.pws.all() or \
                testers_group in obj.groups.all() and request.user.employee.pws.all().first() in obj.employee.pws.all()
        return perm


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


class TestKitAndCertPermChecker(object):
    @staticmethod
    def has_perm(request):
        return request.user.has_perm('webapp.access_to_pws_test_kits') and request.user.has_perm('webapp.access_to_pws_tester_certs')
