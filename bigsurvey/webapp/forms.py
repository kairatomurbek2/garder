from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext as _
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


class HazardFormForTester(forms.ModelForm):
    class Meta:
        model = models.Hazard
        exclude = ('survey', 'hazard_type', 'location1', 'location2', 'notes', 'due_install_test_date')


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


class UserAddForm(UserCreationForm):
    def save(self, commit=True):
        self.instance = super(UserAddForm, self).save()
        self.save_m2m()
        return self.instance

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name', 'groups')


class UserEditForm(UserChangeForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    password = None
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, required=False,
                                help_text=_("If you do not want to change password leave this field blank"))
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput, required=False,
                                help_text=_("Enter the same password as above, for verification."))

    def save(self, commit=True):
        password = self.cleaned_data.get('password1')
        if password:
            self.instance.set_password(password)
        return super(UserEditForm, self).save(commit)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_password(self):
        return self.initial.get('password')

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name', 'groups')