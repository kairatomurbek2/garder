from django import forms
from django.utils.translation import ugettext_lazy as _
import models


class PWSForm(forms.ModelForm):
    number = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=15, label=_("Number"))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=50, label=_("Name"))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'uk-width-1-1'}), max_length=30, label=_("City"))
    water_source = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'uk-width-1-1'}),
                                          queryset=models.SourceType.objects.all(), label=_("Source type"),
                                          empty_label=_("None"))
    notes = forms.CharField(widget=forms.Textarea(attrs={'class': 'uk-width-1-1'}), max_length=255, required=False)

    class Meta:
        model = models.PWS