from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from django import forms
from redactor.widgets import RedactorEditor

import models


class EmployeeInline(admin.StackedInline):
    model = models.Employee
    can_delete = False
    verbose_name_plural = _('Personal Data')
    verbose_name = _('Personal Data')


class EmployeeAdmin(UserAdmin):
    inlines = (EmployeeInline, )


class StaticTextAdminForm(forms.ModelForm):
    class Meta:
        model = models.StaticText
        fields = ['title', 'group', 'text']
        widgets = {
            'text': RedactorEditor(allow_image_upload=True, allow_file_upload=False),
        }


class StaticTextAdmin(admin.ModelAdmin):
    form = StaticTextAdminForm


class SurveyAdminForm(forms.ModelForm):
    class Meta:
        model = models.Survey
        exclude = []

    def __init__(self, *args, **kwargs):
        super(SurveyAdminForm, self).__init__(*args, **kwargs)
        self.fields['hazards'].queryset = models.Hazard.objects.filter(site=self.instance.site)


class SurveyAdmin(admin.ModelAdmin):
    form = SurveyAdminForm
    filter_horizontal = ("hazards",)


class LetterTypeAdmin(admin.ModelAdmin):
    list_display = 'letter_type', 'pws'


admin.site.unregister(User)
admin.site.register(User, EmployeeAdmin)
admin.site.register(models.AssemblyLocation)
admin.site.register(models.BPManufacturer)
admin.site.register(models.BPSize)
admin.site.register(models.BPType)
admin.site.register(models.CustomerCode)
admin.site.register(models.Detail)
admin.site.register(models.FloorsCount)
admin.site.register(models.Hazard)
admin.site.register(models.HazardType)
admin.site.register(models.ICPointType)
admin.site.register(models.Letter)
admin.site.register(models.LetterType, LetterTypeAdmin)
admin.site.register(models.Licence)
admin.site.register(models.Orientation)
admin.site.register(models.PWS)
admin.site.register(models.ServiceType)
admin.site.register(models.Site)
admin.site.register(models.SiteType)
admin.site.register(models.SiteUse)
admin.site.register(models.SourceType)
admin.site.register(models.Special)
admin.site.register(models.Survey, SurveyAdmin)
admin.site.register(models.SurveyType)
admin.site.register(models.Test)
admin.site.register(models.TestManufacturer)
admin.site.register(models.TestModel)
admin.site.register(models.AssemblyStatus)
admin.site.register(models.SiteStatus)
admin.site.register(models.StaticText, StaticTextAdmin)
