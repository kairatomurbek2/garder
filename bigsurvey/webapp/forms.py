from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import models
from main.parameters import Groups, Messages, VALVE_LEAKED_CHOICES, CLEANED_REPLACED_CHOICES, TEST_RESULT_CHOICES, DATEFORMAT_CHOICES
from webapp.validators import validate_excel_file


class PWSForm(forms.ModelForm):
    class Meta:
        model = models.PWS
        fields = '__all__'


class PWSFormForAdmin(forms.ModelForm):
    class Meta:
        model = models.PWS
        exclude = 'number', 'name'


class SiteForm(forms.ModelForm):
    pws = forms.ModelChoiceField(queryset=models.PWS.objects.all(), empty_label=None)

    class Meta:
        model = models.Site
        fields = '__all__'


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


def coerce_to_bool(value):
    return value == 'True'


class TestForm(forms.ModelForm):
    tester = forms.ModelChoiceField(queryset=models.User.objects.filter(groups__name=Groups.tester), empty_label=None)
    cv1_leaked = forms.ChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES, initial=False)
    cv2_leaked = forms.ChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES, initial=False)
    outlet_sov_leaked = forms.ChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES, initial=False)
    cv1_cleaned = forms.TypedChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES,
                                         coerce=coerce_to_bool, initial=True)
    rv_cleaned = forms.TypedChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES,
                                        coerce=coerce_to_bool, initial=True)
    cv2_cleaned = forms.TypedChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES,
                                         coerce=coerce_to_bool, initial=True)
    pvb_cleaned = forms.TypedChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES,
                                         coerce=coerce_to_bool, initial=True)
    rv_did_not_open = forms.BooleanField(initial=False, required=False)
    air_inlet_did_not_open = forms.BooleanField(initial=False, required=False)
    cv_leaked = forms.BooleanField(initial=False, required=False)
    cv1_replaced_details = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                          queryset=models.Detail.objects.all(),
                                                          required=False)
    rv_replaced_details = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                         queryset=models.Detail.objects.all(),
                                                         required=False)
    cv2_replaced_details = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                          queryset=models.Detail.objects.all(),
                                                          required=False)
    pvb_replaced_details = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                          queryset=models.Detail.objects.all(),
                                                          required=False)
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

    def _clean_cv1_cleaned(self):
        cv1_cleaned = self.cleaned_data.get('cv1_cleaned')
        if not cv1_cleaned:
            cv1_replaced_details = self.cleaned_data.get('cv1_replaced_details')
            if not cv1_replaced_details:
                self._custom_errors.append(ValidationError(Messages.Test.cv1_replaced_details_not_provided))

    def _clean_rv_cleaned(self):
        rv_cleaned = self.cleaned_data.get('rv_cleaned')
        if not rv_cleaned:
            rv_replaced_details = self.cleaned_data.get('rv_replaced_details')
            if not rv_replaced_details:
                self._custom_errors.append(ValidationError(Messages.Test.rv_replaced_details_not_provided))

    def _clean_cv2_cleaned(self):
        cv2_cleaned = self.cleaned_data.get('cv2_cleaned')
        if not cv2_cleaned:
            cv2_replaced_details = self.cleaned_data.get('cv2_replaced_details')
            if not cv2_replaced_details:
                self._custom_errors.append(ValidationError(Messages.Test.cv2_replaced_details_not_provided))

    def _clean_pvb_cleaned(self):
        pvb_cleaned = self.cleaned_data.get('pvb_cleaned')
        if not pvb_cleaned:
            pvb_replaced_details = self.cleaned_data.get('pvb_replaced_details')
            if not pvb_replaced_details:
                self._custom_errors.append(ValidationError(Messages.Test.pvb_replaced_details_not_provided))

    def clean(self):
        self._clean_relief_valve()
        self._clean_air_inlet()
        self._clean_cv_leaked()
        self._clean_cv1_cleaned()
        self._clean_rv_cleaned()
        self._clean_cv2_cleaned()
        self._clean_pvb_cleaned()
        if self._custom_errors:
            raise ValidationError(self._custom_errors)
        return super(TestForm, self).clean()

    class Meta:
        model = models.Test
        exclude = ('bp_device', 'rv_opened', 'air_inlet_opened', 'paid', 'user', 'paypal_payment_id')


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


class LetterTypeForm(forms.ModelForm):
    def clean_letter_type(self):
        return self.instance.letter_type

    class Meta:
        model = models.LetterType
        fields = ('template', 'header', 'letter_type')


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


class LetterOptionsForm(forms.Form):
    attach_testers = forms.BooleanField(widget=forms.CheckboxInput, label=_('Attach testers list'), required=False)
    attach_consultant_info = forms.BooleanField(widget=forms.CheckboxInput, label=_('Attach consultant info'), required=False)


class LetterSendForm(LetterOptionsForm):
    send_to = forms.EmailField(required=True, label=_('Send to'))


class ImportForm(forms.Form):
    file = forms.FileField(validators=[validate_excel_file])
    date_format = forms.ChoiceField(choices=DATEFORMAT_CHOICES)
    date_format_other = forms.CharField(required=False)


class ImportMappingsForm(forms.Form):
    model_field = forms.CharField(widget=forms.HiddenInput)
    excel_field = forms.ChoiceField(required=False)


class BaseImportMappingsFormSet(forms.BaseFormSet):
    def add_error(self, error_message):
        self._non_form_errors.append(error_message)

    def clean(self):
        if any(self.errors):
            raise ValidationError(Messages.Import.required_fields_not_filled)
        excel_fields = []
        for form in self.forms:
            excel_field = form.cleaned_data.get('excel_field')
            if excel_field and excel_field in excel_fields:
                raise forms.ValidationError(Messages.Import.duplicate_excel_fields)
            excel_fields.append(excel_field)

    def set_model_fields_labels(self, labels):
        for form, label in zip(self.forms, labels):
            form.fields.get('model_field').label = label

    def set_model_fields_help_texts(self, help_texts):
        for form, help_text in zip(self.forms, help_texts):
            form.fields.get('model_field').help_text = help_text

    def set_required_model_fields(self, required_fields):
        for form in self.forms:
            if form.initial.get('model_field') in required_fields:
                form.fields.get('excel_field').required = True

    def get_mappings(self):
        mappings = {}
        for form in self.forms:
            try:
                model_field = form.cleaned_data.get('model_field')
                excel_field = form.cleaned_data.get('excel_field')
                mappings[model_field] = int(excel_field)
            except ValueError:
                pass
        return mappings

    def set_excel_field_choices(self, choices):
        for form in self.forms:
            form.fields.get('excel_field').choices = [('', '----------')] + choices


class PaymentForm(forms.Form):
    tests = forms.ModelMultipleChoiceField(queryset=models.Test.objects.none(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', models.Test.objects.none())
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['tests'].queryset = queryset
