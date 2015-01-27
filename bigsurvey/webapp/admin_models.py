# Currently not used, left as an example

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
import models


class CoreAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super(CoreAdmin, self).__init__(model, admin_site)
        self.user_groups = None

    def is_superadmin(self, request):
        user_groups = request.user.groups.values_list('name', flat=True)
        if 'SuperAdministrators' in user_groups:
            return True
        else:
            return False

    def get_queryset(self, request):
        qs = super(CoreAdmin, self).get_queryset(request)
        if not self.is_superadmin(request):
            qs = qs.filter(site__pws=request.user.employee.pws)
        return qs

    def has_change_permission(self, request, obj=None):
        if self.is_superadmin(request) or not obj:
            return True
        return False

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'site' and not self.is_superadmin(request):
            kwargs['queryset'] = models.Site.objects.filter(pws=request.user.employee.pws)
        return super(CoreAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class EmployeeInline(admin.StackedInline):
    exclude = []
    model = models.Employee
    can_delete = False
    verbose_name_plural = _('Personal Data')
    verbose_name = _('Personal Data')


class EmployeeAdmin(UserAdmin, CoreAdmin):
    inlines = (EmployeeInline, )

    def save_model(self, request, obj, form, change):
        if not self.is_superadmin(request):
            obj.employee.pws = request.user.employee.pws
        obj.save()

    def get_queryset(self, request):
        qs = models.User.objects.all()
        if not self.is_superadmin(request):
            qs = qs.filter(employee__pws=request.user.employee.pws).exclude(groups__name='SuperAdministrators')
        return qs

    def has_change_permission(self, request, obj=None):
        return super(EmployeeAdmin, self).has_change_permission(request, obj) or \
               obj.employee.pws == request.user.employee.pws and 'SuperAdministrators' not in obj.groups.values_list(
                   'name', flat=True)

    def get_form(self, request, obj=None, **kwargs):
        self.inlines[0].exclude = []
        if not self.is_superadmin(request):
            self.inlines[0].exclude.append('pws')
            self.fieldsets[2][1]['fields'] = ('is_active', 'is_staff', 'groups')

        return super(EmployeeAdmin, self).get_form(request, obj, **kwargs)


class SiteAdmin(CoreAdmin):
    def save_model(self, request, obj, form, change):
        if not self.is_superadmin(request):
            obj.pws = request.user.employee.pws
        obj.save()

    def get_queryset(self, request):
        qs = models.Site.objects.all()
        if not self.is_superadmin(request):
            qs = qs.filter(pws=request.user.employee.pws)
        return qs

    def has_change_permission(self, request, obj=None):
        return super(SiteAdmin, self).has_change_permission(request, obj) or \
               obj.pws == request.user.employee.pws

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not self.is_superadmin(request):
            self.exclude.append('pws')
        return super(SiteAdmin, self).get_form(request, obj, **kwargs)


class InspectionAdmin(CoreAdmin):
    exclude = ['assigned_by']

    def save_model(self, request, obj, form, change):
        obj.assigned_by = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'assigned_to':
            kwargs['queryset'] = models.User.objects.filter(groups__name='Surveyors')
            if not self.is_superadmin(request):
                kwargs['queryset'] = kwargs['queryset'].filter(employee__pws=request.user.employee.pws)
        return super(InspectionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return super(InspectionAdmin, self).has_change_permission(request, obj) or \
               obj.site.pws == request.user.employee.pws


class TestPermissionAdmin(CoreAdmin):
    exclude = ['given_by']

    def save_model(self, request, obj, form, change):
        obj.given_by = request.user
        obj.save()

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'given_to':
            kwargs['queryset'] = models.User.objects.filter(groups__name='Testers')
        return super(TestPermissionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return super(TestPermissionAdmin, self).has_change_permission(request, obj) or \
               obj.site.pws == request.user.employee.pws


class SurveyAdmin(CoreAdmin):
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'surveyor':
            kwargs['queryset'] = models.User.objects.filter(groups__name='Surveyors')
            if not self.is_superadmin(request):
                kwargs['queryset'] = kwargs['queryset'].filter(employee__pws=request.user.employee.pws)
        return super(SurveyAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        return super(SurveyAdmin, self).has_change_permission(request, obj) or \
               obj.site.pws == request.user.employee.pws


class HazardAdmin(CoreAdmin):
    def get_queryset(self, request):
        qs = models.Hazard.objects.all()
        if not self.is_superadmin(request):
            qs = qs.filter(survey__site__pws=request.user.employee.pws)
        return qs

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'survey' and not self.is_superadmin(request):
            kwargs['queryset'] = models.Survey.objects.filter(site__pws=request.user.employee.pws)
        return super(HazardAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class TestAdmin(CoreAdmin):
    def get_queryset(self, request):
        qs = models.Test.objects.all()
        if not self.is_superadmin(request):
            qs = qs.filter(bp_device__survey__site__pws=request.user.employee.pws)
        return qs

    def has_change_permission(self, request, obj=None):
        return super(TestAdmin, self).has_change_permission(request, obj) or \
               obj.bp_device.survey.site.pws == request.user.employee.pws

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'bp_device' and not self.is_superadmin(request):
            kwargs['queryset'] = models.Hazard.objects.filter(survey__site__pws=request.user.employee.pws)
        if db_field.name == 'tester':
            kwargs['queryset'] = models.User.objects.filter(groups__name='Testers')
        return super(TestAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)