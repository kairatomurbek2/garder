from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
import models


class EmployeeInline(admin.StackedInline):
    model = models.Employee
    can_delete = False
    verbose_name_plural = _('Personal Data')
    verbose_name = _('Personal Data')


class EmployeeAdmin(UserAdmin):
    inlines = (EmployeeInline, )


admin.site.unregister(User)
admin.site.register(User, EmployeeAdmin)
admin.site.register(models.AssemblyLocation)
admin.site.register(models.BPManufacturer)
admin.site.register(models.BPSize)
admin.site.register(models.BPType)
admin.site.register(models.Customer)
admin.site.register(models.CustomerCode)
admin.site.register(models.FloorsCount)
admin.site.register(models.Hazard)
admin.site.register(models.HazardType)
admin.site.register(models.ICPointType)
admin.site.register(models.Inspection)
admin.site.register(models.Letter)
admin.site.register(models.LetterType)
admin.site.register(models.Licence)
admin.site.register(models.Orientation)
admin.site.register(models.PWS)
admin.site.register(models.ServiceType)
admin.site.register(models.Site)
admin.site.register(models.SiteType)
admin.site.register(models.SiteUse)
admin.site.register(models.SourceType)
admin.site.register(models.Special)
admin.site.register(models.Survey)
admin.site.register(models.SurveyType)
admin.site.register(models.Test)
admin.site.register(models.TestManufacturer)
admin.site.register(models.TestPermission)
admin.site.register(models.AssemblyStatus)
admin.site.register(models.SiteStatus)
