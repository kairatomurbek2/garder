from django.contrib import admin
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

    def has_change_permission(self, request, obj=None):
        if self.is_superadmin(request) or not obj:
            return True
        return False

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'site' and not self.is_superadmin(request):
            kwargs['queryset'] = models.Site.objects.filter(pws=request.user.employee.pws)
        if db_field.name == 'assigned_to':
            kwargs['queryset'] = models.User.objects.filter(groups__name='Surveyors')
            if not self.is_superadmin(request):
                kwargs['queryset'] = kwargs['queryset'].filter(employee__pws=request.user.employee.pws)
        if db_field.name == 'given_to':
            kwargs['queryset'] = models.User.objects.filter(groups__name='Testers')
        return super(CoreAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SiteAdmin(CoreAdmin):
    def save_model(self, request, obj, form, change):
        if not self.is_superadmin(request):
            obj.pws = request.user.employee.pws
        new = False
        if not obj.id:
            new = True
        obj.save()
        if new:
            potable = models.ServiceType.objects.get(service_type='potable')
            fire = models.ServiceType.objects.get(service_type='fire')
            irrigation = models.ServiceType.objects.get(service_type='irrigation')
            obj.pws_set.add(potable, fire, irrigation)
            obj.save()

    def get_queryset(self, request):
        qs = super(SiteAdmin, self).get_queryset(request)
        if not self.is_superadmin(request):
            qs = qs.filter(pws=request.user.employee.pws)
        return qs

    def has_change_permission(self, request, obj=None):
        return super(SiteAdmin, self).has_change_permission(request, obj) or \
               obj.pws == request.user.employee.pws

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not self.is_superadmin(request):
            self.exclude = ['pws']
        return super(SiteAdmin, self).get_form(request, obj, **kwargs)


class InspectionAdmin(CoreAdmin):
    exclude = ['assigned_by']

    def save_model(self, request, obj, form, change):
        obj.assigned_by = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(InspectionAdmin, self).get_queryset(request)
        if not self.is_superadmin(request):
            qs = qs.filter(site__pws=request.user.employee.pws)
        return qs

    def has_change_permission(self, request, obj=None):
        return super(InspectionAdmin, self).has_change_permission(request, obj) or \
               obj.site.pws == request.user.employee.pws


class TestPermissionAdmin(CoreAdmin):
    exclude = ['given_by']

    def save_model(self, request, obj, form, change):
        obj.given_by = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(TestPermissionAdmin, self).get_queryset(request)
        if not self.is_superadmin(request):
            qs = qs.filter(site__pws=request.user.employee.pws)
        return qs

    def has_change_permission(self, request, obj=None):
        return super(TestPermissionAdmin, self).has_change_permission(request, obj) or \
               obj.site.pws == request.user.employee.pws


class SurveyAdmin(CoreAdmin):
    pass


class HazardAdmin(CoreAdmin):
    pass


class TestAdmin(CoreAdmin):
    pass