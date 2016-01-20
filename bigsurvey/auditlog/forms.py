import datetime
from dateutil.relativedelta import relativedelta
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group
from webapp import models


class AuditLogFilterForm(forms.Form):
    today = datetime.date.today()
    first_day_of_cur_month = today-datetime.timedelta(
        days=today.day-1)
    last_day_of_cur_month = first_day_of_cur_month + relativedelta(
        months=1, days=-1)
    pws = forms.ModelChoiceField(queryset=models.PWS.objects.none(), required=False,
                                 empty_label=_("All available PWSs"), label='PWS')
    start_date = forms.DateField(initial=first_day_of_cur_month)
    end_date = forms.DateField(initial=last_day_of_cur_month)
    username = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'placeholder': _('Enter text fragment')}))
    user_group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, empty_label=_("All user groups"))
    record_object = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={'placeholder': _('Enter text fragment')}))
