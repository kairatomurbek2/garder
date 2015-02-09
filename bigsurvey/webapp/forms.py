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
    customer = forms.CharField()

    def save(self, commit=True):
        customer_id = self.cleaned_data['customer']
        customer = models.Customer.objects.get(pk=customer_id)
        self.instance.customer = customer
        return super(SiteForm, self).save(commit)

    class Meta:
        model = models.Site
        exclude = ('customer',)


class SurveyForm(forms.ModelForm):
    surveyor = forms.ModelChoiceField(queryset=models.User.objects.filter(groups__name=Groups.surveyor), empty_label=None)

    class Meta:
        model = models.Survey
        exclude = ('site', 'service_type')


class HazardForm(forms.ModelForm):
    class Meta:
        model = models.Hazard
        exclude = ('survey',)


class TestForm(forms.ModelForm):
    tester = forms.ModelChoiceField(queryset=models.User.objects.filter(groups__name=Groups.tester), empty_label=None)

    class Meta:
        model = models.Test
        exclude = ('bp_device',)