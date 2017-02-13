from ast import literal_eval
from decimal import Decimal
from datetime import datetime
from django.conf import settings
from cStringIO import StringIO

from django.forms.utils import ErrorList

import models
import os
import re
from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _
from main.parameters import Groups, Messages, VALVE_LEAKED_CHOICES, CLEANED_REPLACED_CHOICES, \
    TEST_RESULT_CHOICES, DATEFORMAT_CHOICES, BP_TYPE, POSSIBLE_IMPORT_MAPPINGS, SITE_STATUS, STATES, \
    TEST_PRICE
from webapp.validators import validate_excel_file
import tarfile


class PWSForm(forms.ModelForm):
    is_active = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}), required=False)

    class Meta:
        model = models.PWS
        fields = '__all__'


class PWSFormForAdmin(forms.ModelForm):
    class Meta:
        model = models.PWS
        exclude = 'number', 'name', 'price'


class SiteForm(forms.ModelForm):
    pws = forms.ModelChoiceField(queryset=models.PWS.active_only.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super(SiteForm, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = None
        self.fields['status'].initial = SITE_STATUS.ACTIVE

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
    hazards = forms.ModelMultipleChoiceField(queryset=models.Hazard.objects.all(), required=False,
                                             widget=forms.CheckboxSelectMultiple(attrs={"checked": ""}))

    class Meta:
        model = models.Survey
        exclude = ('site', 'service_type')


class HazardForm(forms.ModelForm):
    letter_type = forms.ModelChoiceField(queryset=models.LetterType.objects.none(), required=False,
                                         empty_label=_("No letter"))

    def __init__(self, *args, **kwargs):
        letter_types_qs = kwargs.pop('letter_types_qs', False)
        super(HazardForm, self).__init__(*args, **kwargs)
        self.fields['letter_type'].queryset = letter_types_qs

    class Meta:
        model = models.Hazard
        exclude = ('site', 'service_type', 'bp_device')


class HazardFormForSurvey(forms.ModelForm):
    is_present = forms.BooleanField(initial=True, widget=forms.HiddenInput())
    letter_type = forms.ModelChoiceField(queryset=models.LetterType.objects.none(), required=False,
                                         empty_label=_("No letter"))

    def __init__(self, *args, **kwargs):
        letter_types_qs = kwargs.pop('letter_types_qs', False)
        super(HazardFormForSurvey, self).__init__(*args, **kwargs)
        self.fields['letter_type'].queryset = letter_types_qs

    class Meta:
        model = models.Hazard
        exclude = ('site', 'service_type', 'bp_device')


class BPForm(forms.ModelForm):
    class Meta:
        model = models.BPDevice
        fields = ('assembly_location', 'installed_properly', 'installer', 'install_date', 'replace_date',
                  'orientation', 'bp_type_present', 'bp_size', 'manufacturer', 'model_no', 'serial_no',
                  'notes')


def coerce_to_bool(value):
    if value == 'True':
        return True
    elif value == 'False':
        return False
    raise ValueError('Cannot coerce "%s" to bool' % value)


class TestForm(forms.ModelForm):
    tester = forms.ModelChoiceField(queryset=models.User.objects.filter(groups__name=Groups.tester), empty_label=None)
    cv1_leaked = forms.TypedChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES,
                                        coerce=coerce_to_bool, required=False)
    cv2_leaked = forms.TypedChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES,
                                        coerce=coerce_to_bool, required=False)
    outlet_sov_leaked = forms.TypedChoiceField(widget=forms.RadioSelect, choices=VALVE_LEAKED_CHOICES,
                                               coerce=coerce_to_bool, required=False)
    cv1_cleaned = forms.ChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES, required=False)
    rv_cleaned = forms.ChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES, required=False)
    cv2_cleaned = forms.ChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES, required=False)
    pvb_cleaned = forms.ChoiceField(widget=forms.RadioSelect, choices=CLEANED_REPLACED_CHOICES, required=False)
    rv_did_not_open = forms.BooleanField(initial=False, required=False)
    air_inlet_did_not_open = forms.BooleanField(initial=False, required=False)
    cv_leaked = forms.BooleanField(initial=False, required=False)
    test_result = forms.ChoiceField(widget=forms.RadioSelect, choices=TEST_RESULT_CHOICES)

    def __init__(self, **kwargs):
        super(TestForm, self).__init__(**kwargs)
        self._custom_errors = []
        self.bp_type = None

    def _clean_cv1_gauge_pressure(self):
        cv1_gauge_pressure = self.cleaned_data.get('cv1_gauge_pressure')
        test_result = self.cleaned_data.get('test_result', False)
        if cv1_gauge_pressure < 5 and self._cast_string_to_bool(test_result):
            self.add_error('cv1_gauge_pressure', ValidationError(Messages.Test.cv1_gauge_pressure_value_should_be))
            self.add_error('test_result', ValidationError(Messages.Test.cv1_gauge_pressure_value_should_be))

    def _clean_cv2_gauge_pressure(self):
        cv2_gauge_pressure = self.cleaned_data.get('cv2_gauge_pressure')
        test_result = self.cleaned_data.get('test_result', False)
        if cv2_gauge_pressure < 1 and self._cast_string_to_bool(test_result):
            self.add_error('cv2_gauge_pressure', ValidationError(Messages.Test.cv2_gauge_pressure_value_should_be))
            self.add_error('test_result', ValidationError(Messages.Test.cv2_gauge_pressure_value_should_be))

    def _clean_cv1_retest_gauge_pressure(self):
        cv1_retest_gauge_pressure = self.cleaned_data.get('cv1_retest_gauge_pressure')
        test_result = self.cleaned_data.get('test_result', False)
        if cv1_retest_gauge_pressure < 5 and self._cast_string_to_bool(test_result):
            self.add_error('cv1_retest_gauge_pressure',
                           ValidationError(Messages.Test.cv1_retest_gauge_pressure_value_should_be))
            self.add_error('test_result', ValidationError(Messages.Test.cv1_retest_gauge_pressure_value_should_be))

    def _clean_rv_psi2(self):
        rv_psi2 = self.cleaned_data.get('rv_psi2')
        test_result = self.cleaned_data.get('test_result', False)
        if rv_psi2 < 2 and self._cast_string_to_bool(test_result):
            self.add_error('rv_psi2', ValidationError(Messages.Test.rv_psi2_value_should_be))
            self.add_error('test_result', ValidationError(Messages.Test.rv_psi2_value_should_be))

    def _clean_cv2_retest_gauge_pressure(self):
        cv2_retest_gauge_pressure = self.cleaned_data.get('cv2_retest_gauge_pressure')
        test_result = self.cleaned_data.get('test_result', False)
        if cv2_retest_gauge_pressure < 1 and self._cast_string_to_bool(test_result):
            self.add_error('cv2_retest_gauge_pressure',
                           ValidationError(Messages.Test.cv2_retest_gauge_pressure_value_should_be))
            self.add_error('test_result', ValidationError(Messages.Test.cv2_retest_gauge_pressure_value_should_be))

    def _clean_rv_did_not_open(self):
        rv_did_not_open = self.cleaned_data.get('rv_did_not_open', False)
        test_result = self.cleaned_data.get('test_result', False)
        if rv_did_not_open:
            self.cleaned_data.pop('rv_psi1', None)
            self.instance.rv_psi1 = None
            self.instance.rv_opened = False
        else:
            self.instance.rv_opened = True
            rv_psi1 = self.cleaned_data.get('rv_psi1')
            if rv_psi1 is None:
                self.add_error('rv_did_not_open', ValidationError(Messages.Test.rv_not_provided))
            elif rv_psi1 < 2 and self._cast_string_to_bool(test_result):
                self.add_error('rv_psi1', ValidationError(Messages.Test.rv_psi1_value_should_be_gte_two))
                self.add_error('test_result', ValidationError(Messages.Test.rv_psi1_value_should_be_gte_two))

    def _clean_air_inlet_did_not_open(self):
        air_inlet_did_not_open = self.cleaned_data.get('air_inlet_did_not_open', False)
        test_result = self.cleaned_data.get('test_result', False)
        if air_inlet_did_not_open:
            self.cleaned_data.pop('air_inlet_psi', None)
            self.instance.air_inlet_psi = None
            self.instance.air_inlet_opened = False
        else:
            self.instance.air_inlet_opened = True
            air_inlet_psi = self.cleaned_data.get('air_inlet_psi')
            if air_inlet_psi is None:
                self.add_error('air_inlet_did_not_open', ValidationError(Messages.Test.air_inlet_not_provided))
            elif air_inlet_psi < 1 and self._cast_string_to_bool(test_result):
                self.add_error('air_inlet_psi', ValidationError(Messages.Test.air_inlet_psi_value_should_be))
                self.add_error('test_result', ValidationError(Messages.Test.air_inlet_psi_value_should_be))

    def _clean_cv_leaked(self):
        cv_leaked = self.cleaned_data.get('cv_leaked', False)
        test_result = self.cleaned_data.get('test_result', False)
        if cv_leaked:
            self.cleaned_data.pop('cv_held_pressure', None)
            self.instance.cv_held_pressure = None
        else:
            cv_held_pressure = self.cleaned_data.get('cv_held_pressure')
            if cv_held_pressure is None:
                self.add_error('cv_leaked', ValidationError(Messages.Test.cv_not_provided))
            elif cv_held_pressure < 1 and self._cast_string_to_bool(test_result):
                self.add_error('cv_leaked', ValidationError(Messages.Test.cv_leaked_value_should_be))
                self.add_error('test_result', ValidationError(Messages.Test.cv_leaked_value_should_be))

    def _clean_air_inlet_retest_psi(self):
        air_inlet_retest_psi = self.cleaned_data.get('air_inlet_retest_psi')
        test_result = self.cleaned_data.get('test_result', False)
        if air_inlet_retest_psi < 1 and self._cast_string_to_bool(test_result):
            self.add_error('air_inlet_retest_psi', ValidationError(Messages.Test.air_inlet_retest_psi_value_should_be))
            self.add_error('test_result', ValidationError(Messages.Test.air_inlet_retest_psi_value_should_be))

    def _clean_cv_retest_psi(self):
        cv_retest_psi = self.cleaned_data.get('cv_retest_psi')
        test_result = self.cleaned_data.get('test_result', False)
        if cv_retest_psi < 1 and self._cast_string_to_bool(test_result):
            self.add_error('cv_retest_psi', ValidationError(Messages.Test.cv_retest_psi_value_should_be))
            self.add_error('test_result', ValidationError(Messages.Test.cv_retest_psi_value_should_be))

    def _clean_cv1_leaked(self):
        cv1_leaked = self.cleaned_data.get('cv1_leaked')
        test_result = self.cleaned_data.get('test_result', False)
        if cv1_leaked == self.fields['cv1_leaked'].empty_value:
            self.add_error('cv1_leaked',
                           ValidationError(self.fields['cv1_leaked'].error_messages['required'], code='required'))
        if cv1_leaked and self._cast_string_to_bool(test_result):
            error_message = Messages.Test.cv1_leaked_and_passed_error
            self.add_error('cv1_leaked', ValidationError(error_message))
            self.add_error('test_result', ValidationError(error_message))

    def _clean_cv2_leaked(self):
        cv2_leaked = self.cleaned_data.get('cv2_leaked')
        test_result = self.cleaned_data.get('test_result', False)
        if cv2_leaked == self.fields['cv2_leaked'].empty_value:
            self.add_error('cv2_leaked',
                           ValidationError(self.fields['cv2_leaked'].error_messages['required'], code='required'))
        if cv2_leaked and self._cast_string_to_bool(test_result):
            error_message = Messages.Test.cv2_leaked_and_passed_error
            self.add_error('cv2_leaked', ValidationError(error_message))
            self.add_error('test_result', ValidationError(error_message))

    def _clean_outlet_sov_leaked(self):
        outlet_sov_leaked = self.cleaned_data.get('outlet_sov_leaked')
        test_result = self.cleaned_data.get('test_result', False)
        if outlet_sov_leaked == self.fields['outlet_sov_leaked'].empty_value:
            self.add_error('outlet_sov_leaked',
                           ValidationError(self.fields['outlet_sov_leaked'].error_messages['required'],
                                           code='required'))
        if outlet_sov_leaked and self._cast_string_to_bool(test_result):
            error_message = Messages.Test.outlet_sov_leaked_and_passed_error
            self.add_error('outlet_sov_leaked', ValidationError(error_message))
            self.add_error('test_result', ValidationError(error_message))

    def _clean_valve_cleaned(self, type, error_message):
        field_name = '%s_cleaned' % type
        value = self.cleaned_data.get(field_name)
        if value in self.fields[field_name].empty_values:
            self.add_error(field_name,
                           ValidationError(self.fields[field_name].error_messages['required'], code='required'))
        if value == u'2':
            details = [value for key, value in self.cleaned_data.items() if key.startswith('%s_detail' % type)]
            if not any(details):
                self.add_error(field_name, ValidationError(error_message))

    def _clean_cv1_cleaned(self):
        self._clean_valve_cleaned('cv1', Messages.Test.cv1_replaced_details_not_provided)

    def _clean_rv_cleaned(self):
        self._clean_valve_cleaned('rv', Messages.Test.rv_replaced_details_not_provided)

    def _clean_cv2_cleaned(self):
        self._clean_valve_cleaned('cv2', Messages.Test.cv2_replaced_details_not_provided)

    def _clean_pvb_cleaned(self):
        self._clean_valve_cleaned('pvb', Messages.Test.pvb_replaced_details_not_provided)

    def clean_rp_types(self):
        self._clean_cv1_leaked()
        self._clean_cv2_leaked()
        self._clean_outlet_sov_leaked()
        self._clean_rv_did_not_open()
        self._clean_cv1_cleaned()
        self._clean_cv2_cleaned()
        self._clean_rv_cleaned()
        self._clean_cv1_gauge_pressure()
        self._clean_cv2_gauge_pressure()
        self._clean_cv1_retest_gauge_pressure()
        self._clean_rv_psi2()
        self._clean_cv2_retest_gauge_pressure()

    def clean_dc_types(self):
        self._clean_cv1_cleaned()
        self._clean_cv2_cleaned()

    def clean_standalone_types(self):
        self._clean_cv_leaked()
        self._clean_air_inlet_did_not_open()
        self._clean_pvb_cleaned()
        self._clean_air_inlet_retest_psi()
        self._clean_cv_retest_psi()

    def clean(self):
        if self.bp_type in BP_TYPE.RP_TYPES:
            self.clean_rp_types()
        if self.bp_type in BP_TYPE.DC_TYPES:
            self.clean_dc_types()
        if self.bp_type in BP_TYPE.STANDALONE_TYPES:
            self.clean_standalone_types()
        return super(TestForm, self).clean()

    @staticmethod
    def _cast_string_to_bool(value):
        return literal_eval(value) if value == u'False' or value == u'True' else value

    class Meta:
        model = models.Test
        exclude = ('bp_device', 'rv_opened', 'air_inlet_opened', 'paid', 'user', 'price', 'paypal_payment_id')


class EmployeeForm(forms.ModelForm):
    pws = forms.ModelMultipleChoiceField(models.PWS.active_only.all(), required=True, label=_('PWS'))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', False)
        super(EmployeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Employee
        exclude = ('user',)


class EmployeeFormNoPWS(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', False)
        super(EmployeeFormNoPWS, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Employee
        exclude = ('user',)


class UserAddForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    groups = forms.ModelMultipleChoiceField(queryset=models.Group.objects.all(), required=True)

    def save(self, commit=True):
        self.instance = super(UserAddForm, self).save()
        self.save_m2m()
        return self.instance

    def clean_email(self):
        data = self.cleaned_data['email']
        if models.User.objects.filter(email=data).exists():
            raise ValidationError(
                _("User with such email already exists"),
                code='email_used'
            )
        return data

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)

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
    is_active = forms.BooleanField(label=_("Active"), widget=forms.CheckboxInput, required=False, initial=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    groups = forms.ModelMultipleChoiceField(queryset=models.Group.objects.all(), required=True)

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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', False)
        super(UserEditForm, self).__init__(*args, **kwargs)
        if user:
            if self._user_is_admin_or_pws_owner(user):
                self.fields['groups'].required = False

    @staticmethod
    def _user_is_admin_or_pws_owner(user):
        is_admin = Groups.admin in [group.name for group in user.groups.all()]
        is_pws_owner = Groups.pws_owner in [group.name for group in user.groups.all()]
        return is_admin or is_pws_owner

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name', 'groups', 'is_active')


class BatchUpdateForm(forms.Form):
    date = forms.DateField(label=_('Select date'), required=False)
    empty_date = forms.BooleanField(label=_('Empty date'), required=False)


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
    pws = forms.ModelChoiceField(queryset=models.PWS.active_only.all(), required=True)
    address = forms.CharField(label=_('Street number and address'), required=False)
    cust_number = forms.CharField(label=_('Customer number'), required=False)
    meter_number = forms.CharField(label=_('Meter number'), required=False)
    bp_device_serial_no = forms.CharField(label=_('BP Device Serial No'), required=False)

    search_field_and_value = None

    def clean(self):
        cleaned_data = super(TesterSiteSearchForm, self).clean()
        address = cleaned_data.get('address')
        cust_number = cleaned_data.get('cust_number')
        meter_number = cleaned_data.get('meter_number')
        bp_device_serial_no = cleaned_data.get('bp_device_serial_no')

        if len(address) == 0 and len(cust_number) == 0 and len(meter_number) == 0 and len(bp_device_serial_no) == 0:
            search_fields = "%s, %s, %s, %s" % (self.fields['address'].label,
                                                self.fields['cust_number'].label,
                                                self.fields['meter_number'].label,
                                                self.fields['bp_device_serial_no'].label)
            error_message = Messages.Site.search_error_fields_not_filled % search_fields
            self.add_error('address', ValidationError(error_message))
            self.add_error('cust_number', ValidationError(error_message))
            self.add_error('meter_number', ValidationError(error_message))
            self.add_error('bp_device_serial_no', ValidationError(error_message))
        else:
            self.search_field_and_value = [{field_name: cleaned_data.get(field_name)}
                                           for field_name in self.fields
                                           if field_name != 'pws' and len(cleaned_data.get(field_name)) > 0]
            if len(self.search_field_and_value) > 1:
                field_names = ["".join(pair.keys()) for pair in self.search_field_and_value]
                labels = [self.fields[field_name].label for field_name in field_names]
                for field_name in field_names:
                    error_message = Messages.Site.search_error_more_than_one_field_filled % ", ".join(labels)
                    self.add_error(field_name, ValidationError(error_message))
            else:
                self.search_field_and_value = self.search_field_and_value[0]
        return cleaned_data


class LetterOptionsForm(forms.Form):
    attach_testers = forms.BooleanField(widget=forms.CheckboxInput, label=_('Attach testers list'), required=False)
    attach_consultant_info = forms.BooleanField(widget=forms.CheckboxInput, label=_('Attach consultant info'),
                                                required=False)


class LetterSendForm(LetterOptionsForm):
    send_to = forms.EmailField(required=True, label=_('Send to'))


class ImportForm(forms.Form):
    file = forms.FileField(validators=[validate_excel_file])
    date_format = forms.ChoiceField(choices=DATEFORMAT_CHOICES)
    date_format_other = forms.CharField(required=False)
    update_only = forms.BooleanField(required=False, initial=False)


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
        req_forms = []
        non_req_forms = []
        for form in self.forms:
            if form.initial.get('model_field') in required_fields:
                form.fields.get('excel_field').required = True
                req_forms.append(form)
            else:
                non_req_forms.append(form)
        self.forms = req_forms + non_req_forms

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
        self.set_formatted_choices(choices)
        for form in self.forms:
            form.fields.get('excel_field').choices = [('', '----------')] + choices
            form.fields.get('excel_field').initial = self.get_initial_for_excel_field(form.fields.get('model_field'))

    def set_formatted_choices(self, choices):
        formatted_choices = []
        for choice in choices:
            choice_label = re.sub('[^0-9a-zA-Z]+', '', choice[1]).lower()
            formatted_choices.append((choice[0], choice_label))
        self.formatted_choices = formatted_choices

    def get_initial_for_excel_field(self, model_field):
        for choice in self.formatted_choices:
            possible_labels = POSSIBLE_IMPORT_MAPPINGS[model_field.label]
            if choice[1] in possible_labels:
                return choice[0]
        return ''


class PaymentForm(forms.Form):
    tests = forms.ModelMultipleChoiceField(queryset=models.Test.objects.none(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', models.Test.objects.none())
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['tests'].queryset = queryset


class UserSearchForm(forms.Form):
    group = forms.ModelChoiceField(queryset=models.Group.objects.filter(
        name__in=(Groups.admin, Groups.surveyor, Groups.tester)
    ), required=True)
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length=30, required=False)
    cert_number = forms.CharField(max_length=128, required=False)

    prefix = 'search'

    def is_valid(self):
        valid = super(UserSearchForm, self).is_valid()
        if valid:
            if self.is_empty(self.cleaned_data['email']) and self.is_empty(self.cleaned_data['username']):
                self.add_error(None, _('Either username or email is required'))
                return False
        return valid

    def is_empty(self, value):
        return value == '' or value is None


class UserInviteForm(forms.Form):
    pws = forms.ModelMultipleChoiceField(queryset=models.PWS.active_only.none(), required=True, label=_('PWS'))
    user = forms.ModelChoiceField(queryset=models.User.objects.all(), required=True)
    prefix = 'invite'

    def __init__(self, *args, **kwargs):
        pws_queryset = kwargs.pop('pws_queryset', models.PWS.active_only.none())
        users = kwargs.pop('users', models.User.objects.none())
        super(UserInviteForm, self).__init__(*args, **kwargs)
        self.fields['pws'].queryset = pws_queryset
        self.fields['user'].queryset = users

    def is_valid(self):
        valid = super(UserInviteForm, self).is_valid()
        if valid:
            user = self.cleaned_data['user']
            selected_pws = self.cleaned_data['pws']
            if set(selected_pws).issubset(user.employee.pws.all()):
                self.add_error(None, Messages.UserInvite.user_already_in_pws)
                return False
        return valid


class TesterCertForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', False)
        super(TesterCertForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.TesterCert
        exclude = ('user',)


class TestKitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', False)
        super(TestKitForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.TestKit
        exclude = ('user',)


class PasswordChangeWithMinLengthForm(PasswordChangeForm):
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if len(new_password1) < 5:
            raise forms.ValidationError(
                _("Your password must be at least 5 characters long"))
        if new_password1 and new_password1 != new_password2:
            raise forms.ValidationError(
                _("Repeat password is not same with new password!"))
        return new_password2


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError(
                _("There is no user registered with the specified email address!"))
        return email


class TestPriceForm(forms.ModelForm):
    pws_multiple = forms.ModelMultipleChoiceField(label='PWS',
                                                  queryset=models.PWS.objects.all(),
                                                  required=False,
                                                  widget=forms.SelectMultiple(
                                                      attrs={'class': 'js-select2-multiple'})
                                                  )
    price=forms.DecimalField(required=True,min_value=0,decimal_places=2,max_digits=7,label='Price',initial=Decimal(5))
    class Meta:
        model=models.PriceHistory
        fields=[]

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            self.add_error('price', _('Price per Test can not be lower than 0'))
        pws_list = self.cleaned_data.get('pws_multiple')
        if pws_list:
            for pws in pws_list:
                if not self.validate_price(price, pws):
                    break
        else:
            self.validate_price(price, pws=None)
        return price

    def validate_price(self, price, pws):
        current_price = models.PriceHistory.current_for_test(pws)
        if current_price:
            if price == current_price.price:
                self.add_error('price', _('New Price can not be the same as the current Price'))
                return False
        return True

    def save_price(self, pws=None):
        current_price = models.PriceHistory.current_for_test(pws)
        price=self.cleaned_data['price']
        if current_price:
            current_date = datetime.now().date()
            if current_date == current_price.start_date:
                current_price.price = price
            else:
                self.instance.price_type = TEST_PRICE
                self.instance.price=price
                self.object = self.save(commit=False)
                self.object.pws = pws
                new_price = models.PriceHistory()
                new_price.save_price_object(self.object)
                current_price.end_date = new_price.start_date
            current_price.save()
        else:
            self.instance.price_type = TEST_PRICE
            self.instance.price = price
            self.object = self.save(commit=False)
            self.object.pws = pws
            models.PriceHistory().save_price_object(self.object)

    def save_multiple(self):
        pws_list = self.cleaned_data.get('pws_multiple')
        for pws in pws_list:
            self.save_price(pws)


class PWSOwnerRegistrationForm(forms.ModelForm):
    number = forms.CharField(max_length=15, required=True, label=_('PWS Number'),
                             widget=forms.TextInput(attrs={'placeholder': _(' LL9999999')}))
    name = forms.CharField(max_length=50, required=True, label=_('Water System Name'))
    county = forms.CharField(max_length=100, required=True)
    office_address = forms.CharField(max_length=50, required=True, label=_('Address'))
    city = forms.CharField(max_length=30, required=True)
    state = forms.ChoiceField(choices=STATES, required=True)
    zip = forms.CharField(max_length=10, required=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=_(
                                     "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone = forms.CharField(validators=[phone_regex], max_length=20, required=True, label=_('Phone Number'))

    class Meta:
        model = models.PWS
        fields = ('number', 'name', 'office_address', 'city', 'state', 'zip', 'phone')


class PWSUserAddForm(UserCreationForm):
    captcha = ReCaptchaField()

    def __init__(self, *args, **kwargs):

        super(PWSUserAddForm, self).__init__(*args, **kwargs)
        if not settings.USE_CAPTHCA:
            del self.fields['captcha']

    def clean_email(self):
        data = self.cleaned_data['email']
        if models.User.objects.filter(email=data).exists():
            raise ValidationError(
                _("User with such email already exists"),
                code='email_used'
            )
        return data

    class Meta:
        model = models.User
        fields = ('username', 'email', 'first_name', 'last_name', 'groups')


class BackupForm(forms.Form):
    backup = forms.ChoiceField(label=_('Backups Available'))
    upload_backup = forms.FileField(label=_('Upload Backup'), required=False)

    def __init__(self, *args, **kwargs):
        super(BackupForm, self).__init__(*args, **kwargs)
        files = os.listdir(settings.BACKUPS_DIR)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(settings.BACKUPS_DIR, x)), reverse=True)
        self.fields["backup"].choices = zip(files, files)

    def is_valid(self):
        valid = super(BackupForm, self).is_valid()
        if valid:
            backup = self.cleaned_data.get("upload_backup")
            if backup:
                backup_data = StringIO()
                for chunk in backup.chunks():
                    backup_data.write(chunk)
                backup_data.seek(0)
                try:
                    tar = tarfile.open(fileobj=backup_data, mode='r:gz')
                    tar_content = tar.getnames()
                    if 'bigsurvey' in tar_content:
                        matcher = re.compile("^bigsurvey_")
                        if any(matcher.match(name) for name in tar_content):
                            return True
                    self.errors['upload_backup'] = _('ERROR: Backup contents are missing')
                    backup_data.close()
                    return False
                except tarfile.TarError:
                    self.errors['upload_backup'] = _('ERROR: Backup is corrupt or is not archive')
                    backup_data.close()
                    return False
        return valid


def count(ids):
    res = []
    for i in range(len(ids)):
        if i < 3:
            res.append(ids[i])
    return res


class BackupPWSOwnerForm(forms.Form):
    time_stamp = forms.ModelChoiceField(queryset=None, label=_('Select Backup'))

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False):
        super(BackupPWSOwnerForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                                 empty_permitted)

        ids = models.Backup.objects.all().order_by('-pk').values_list('pk', flat=True)
        self.fields['time_stamp'].queryset = models.Backup.objects.filter(pk__in=count(ids))
