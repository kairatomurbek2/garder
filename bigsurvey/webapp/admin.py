from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from django import forms
from reversion_compare.admin import CompareVersionAdmin
from bigsurveyadminsite import admin_site_bigsurvey
from ajax_select.fields import AutoCompleteSelectField
from ajax_select import make_ajax_form

import models


class EmployeeInline(admin.StackedInline):
    model = models.Employee
    can_delete = False
    verbose_name_plural = _('Personal Data')
    verbose_name = _('Personal Data')


class EmployeeAdmin(UserAdmin):
    inlines = (EmployeeInline,)


class SurveyAdminForm(forms.ModelForm):
    site = AutoCompleteSelectField('site', required=False, help_text=None)

    class Meta:
        model = models.Survey
        exclude = []

    def __init__(self, *args, **kwargs):
        super(SurveyAdminForm, self).__init__(*args, **kwargs)
        self.fields['hazards'].queryset = models.Hazard.objects.filter(site=self.instance.site)


class HazardAdmin(admin.ModelAdmin):
    form = make_ajax_form(models.Hazard, {'site': 'site'})

class LetterAdmin(admin.ModelAdmin):
    form = make_ajax_form(models.Letter, {'site': 'site','hazard':'hazard'})


class SurveyAdmin(CompareVersionAdmin):
    form = SurveyAdminForm
    filter_horizontal = ("hazards",)


class TestAdmin(CompareVersionAdmin):
    readonly_fields = 'paypal_payment_id',


class ImportLogModelAdmin(CompareVersionAdmin):
    readonly_fields = 'added_sites', 'updated_sites', 'deleted_sites', 'progress'


class LetterTypeAdmin(CompareVersionAdmin):
    list_display = 'letter_type', 'pws'


class PriceAdmin(CompareVersionAdmin):
    list_display = 'price', 'price_type', 'pws', 'start_date', 'end_date'


class TermsConditionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 2:
            return False
        else:
            return True


admin_site_bigsurvey.unregister(User)
admin_site_bigsurvey.register(User, EmployeeAdmin)
admin_site_bigsurvey.register(models.AssemblyLocation)
admin_site_bigsurvey.register(models.BPManufacturer)
admin_site_bigsurvey.register(models.BPSize)
admin_site_bigsurvey.register(models.CustomerCode)
admin_site_bigsurvey.register(models.FloorsCount)
admin_site_bigsurvey.register(models.Hazard,HazardAdmin)
admin_site_bigsurvey.register(models.Regulation)
admin_site_bigsurvey.register(models.HazardType)
admin_site_bigsurvey.register(models.ICPointType)
admin_site_bigsurvey.register(models.Letter,LetterAdmin)
admin_site_bigsurvey.register(models.LetterType, LetterTypeAdmin)
admin_site_bigsurvey.register(models.Orientation)
admin_site_bigsurvey.register(models.PWS)
admin_site_bigsurvey.register(models.ServiceType)
admin_site_bigsurvey.register(models.Site)
admin_site_bigsurvey.register(models.SiteType)
admin_site_bigsurvey.register(models.SiteUse)
admin_site_bigsurvey.register(models.SourceType)
admin_site_bigsurvey.register(models.Special)
admin_site_bigsurvey.register(models.Survey, SurveyAdmin)
admin_site_bigsurvey.register(models.SurveyType)
admin_site_bigsurvey.register(models.Test, TestAdmin)
admin_site_bigsurvey.register(models.TestManufacturer)
admin_site_bigsurvey.register(models.TestModel)
admin_site_bigsurvey.register(models.AssemblyStatus)
admin_site_bigsurvey.register(models.SiteStatus)
admin_site_bigsurvey.register(models.StaticText)
admin_site_bigsurvey.register(models.ImportLog)
admin_site_bigsurvey.register(models.Invite)
admin_site_bigsurvey.register(models.TesterCert)
admin_site_bigsurvey.register(models.TestKit)
admin_site_bigsurvey.register(models.BPDevice)
admin_site_bigsurvey.register(models.PriceHistory, PriceAdmin)
admin_site_bigsurvey.register(models.TermsConditions, TermsConditionAdmin)
