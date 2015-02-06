from django import forms
import models
from main.parameters import Groups


class PWSForm(forms.ModelForm):
    class Meta:
        model = models.PWS


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer


class SiteForm(forms.ModelForm):
    pws = forms.ModelChoiceField(queryset=models.PWS.objects.all(), empty_label=None)

    class Meta:
        model = models.Site


class SurveyForm(forms.ModelForm):
    surveyor = forms.ModelChoiceField(queryset=models.User.objects.filter(groups__name=Groups.surveyor), empty_label=None)

    class Meta:
        model = models.Survey
        exclude = ('site', 'service_type')


class HazardForm(forms.ModelForm):
    class Meta:
        model = models.Hazard
        exclude = ('survey',)

fields = ('bp_type_present', 'bp_type_required', 'bp_size', 'manufacturer', 'installer', 'install_date', 'replace_date', 'orientation', 'model_no', 'serial_no', 'assembly_location', 'assembly_status')