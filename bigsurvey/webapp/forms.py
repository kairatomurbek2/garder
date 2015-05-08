from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import models
from main.parameters import Groups, Messages, VALVE_LEAKED_CHOICES, VALVE_OPENED_CHOICES, CLEANED_REPLACED_CHOICES, Details, TEST_RESULT_CHOICES


class PWSForm(forms.ModelForm):
    class Meta:
        model = models.PWS
        fields = '__all__'


class SiteForm(forms.ModelForm):
    pws = forms.ModelChoiceField(queryset=models.PWS.objects.all(), empty_label=None)

    class Meta:
        model = models.Site


class SiteFormForSurveyor(forms.ModelForm):
    class Meta:
        model = models.Site
        fields = ('potable_present', 'fire_present', 'irrigation_present')


class SurveyForm(forms.ModelForm):
    surveyor = forms.ModelChoiceField(queryset=models.User.objects.filter(groups__name=Groups.surveyor),
                                      empty_label=None)
    hazards = forms.ModelMultipleChoiceField(queryset=models.Hazard.objects.all(), required=False)

    class Meta:
        model = models.Survey
        exclude = ('site', 'service_type')


class HazardForm(forms.ModelForm):
    class Meta:
        model = models.Hazard
        exclude = ('site', 'service_type', 'is_present',)


class HazardFormForTester(forms.ModelForm):
    class Meta:
        model = models.Hazard
        exclude = (
            'site',
            'service_type',
            'hazard_type',
            'location1',
            'location2',
            'notes',
            'due_install_test_date',
            'bp_type_required',
            'is_present',
        )


class TestForm(forms.ModelForm):
    tester = forms.ModelChoiceField(queryset=models.User.objects.filter(groups__name=Groups.tester), empty_label=None)
    cv1_leaked = forms.ChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES, initial=False)
    cv2_leaked = forms.ChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES, initial=False)
    outlet_sov_leaked = forms.ChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES, initial=False)
    cv1_cleaned = forms.ChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES, initial=True)
    rv_cleaned = forms.ChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES, initial=True)
    cv2_cleaned = forms.ChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES, initial=True)
    pvb_cleaned = forms.ChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES, initial=True)
    rv_did_not_open = forms.BooleanField(initial=False, required=False)
    air_inlet_did_not_open = forms.BooleanField(initial=False, required=False)
    cv_leaked = forms.BooleanField(initial=False, required=False)
    cv1_replaced_details = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=models.Detail.objects.get_details_by_pks(Details.cv1), required=False)
    rv_replaced_details = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=models.Detail.objects.get_details_by_pks(Details.rv), required=False)
    cv2_replaced_details = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=models.Detail.objects.get_details_by_pks(Details.cv2), required=False)
    pvb_replaced_details = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=models.Detail.objects.get_details_by_pks(Details.pvb), required=False)
    test_result = forms.ChoiceField(widget=forms.RadioSelect, choices=TEST_RESULT_CHOICES)

    def __init__(self, **kwargs):
        super(TestForm, self).__init__(**kwargs)
        self._custom_errors = []

    def _clean_relief_valve(self):
        rv_did_not_open = self.cleaned_data.get('rv_did_not_open', False)
        if rv_did_not_open:
            self.cleaned_data.pop('rv_psi1', None)
            self.instance.rv_psi1 = None
            self.instance.rv_opened = False
        else:
            self.instance.rv_opened = True
            rv_psi1 = self.cleaned_data.get('rv_psi1')
            if rv_psi1 is None:
                self._custom_errors.append(ValidationError(Messages.Test.rv_not_provided))

    def _clean_air_inlet(self):
        air_inlet_did_not_open = self.cleaned_data.get('air_inlet_did_not_open', False)
        if air_inlet_did_not_open:
            self.cleaned_data.pop('air_inlet_psi', None)
            self.instance.air_inlet_psi = None
            self.instance.air_inlet_opened = False
        else:
            self.instance.air_inlet_opened = True
            air_inlet_psi = self.cleaned_data.get('air_inlet_psi')
            if air_inlet_psi is None:
                self._custom_errors.append(ValidationError(Messages.Test.air_inlet_not_provided))

    def _clean_cv_leaked(self):
        cv_leaked = self.cleaned_data.get('cv_leaked', False)
        if cv_leaked:
            self.cleaned_data.pop('cv_held_pressure', None)
            self.instance.cv_held_pressure = None
        else:
            cv_held_pressure = self.cleaned_data.get('cv_held_pressure')
            if cv_held_pressure is None:
                self._custom_errors.append(ValidationError(Messages.Test.cv_not_provided))

    def clean(self):
        self._clean_relief_valve()
        self._clean_air_inlet()
        self._clean_cv_leaked()
        if self._custom_errors:
            raise ValidationError(self._custom_errors)
        return super(TestForm, self).clean()

    class Meta:
        model = models.Test
        exclude = ('bp_device', 'rv_opened', 'air_inlet_opened')


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


class BatchUpdateForm(forms.Form):
    date = forms.DateField(label=_('Select date'))


class LetterForm(forms.ModelForm):
    hazard = forms.ModelChoiceField(models.Hazard.objects.all(), empty_label=None, required=True)

    class Meta:
        model = models.Letter
        fields = ('letter_type', 'hazard')


class TesterSiteSearchForm(forms.Form):
    pws = forms.ModelChoiceField(queryset=models.PWS.objects.all(), required=False)
    cust_number = forms.CharField(label=_('Customer Number'), required=False)

    site = None

    def clean(self):
        try:
            self.site = models.Site.objects.get(
                pws=self.cleaned_data['pws'],
                cust_number=self.cleaned_data['cust_number']
            )
        except models.Site.DoesNotExist:
            raise ValidationError(Messages.Site.not_found)
        return super(TesterSiteSearchForm, self).clean()


class LetterSendForm(forms.Form):
    send_to = forms.EmailField(required=True)