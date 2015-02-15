from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group
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
        customer_id = self.cleaned_data.get('customer')
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


class InspectionForm(forms.ModelForm):
    class Meta:
        model = models.Inspection
        exclude = ('assigned_by', 'site')


class TestPermissionForm(forms.ModelForm):
    class Meta:
        model = models.TestPermission
        exclude = ('given_by', 'site')


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        exclude = ('user',)


class UserForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, initial='')
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput, initial='',
                                help_text=_("Enter the same password as above, for verification."))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.pk is None:
            return username
        if self.Meta.model.objects.exclude(pk=self.instance.pk).filter(username=username).count():
            raise ValidationError(_('User with this username already exists.'))
        else:
            return username

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name', 'groups')