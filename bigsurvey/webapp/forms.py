from django import forms
import models


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