import os
from subprocess import call

import shutil
from django.conf import settings
from django.forms import ModelChoiceField
from main.parameters import Messages
from webapp import forms, models
from webapp.views import BaseFormView, reverse, HttpResponseRedirect
from django.contrib import messages


class BackupPWSOwner(BaseFormView):
    success_message = Messages.PWS.backup_success
    permission = 'webapp.browse_backup'
    template_name = 'backup.html'
    form_class = forms.BackupPWSOwnerForm
    model = models.Backup

    def get_form(self, form_class):
        form = super(BackupPWSOwner, self).get_form(form_class)
        if self.request.user.has_perm('webapp.access_to_all_sites'):
            form.fields['pws'] = ModelChoiceField(queryset=models.PWS.active_only.all())
        elif self.request.user.has_perm('webapp.browse_backup'):
            form.fields['pws'] = ModelChoiceField(queryset=self.request.user.employee.pws.all())
        return form

    def form_valid(self, form):
        python_path = settings.PYTHON_PATH
        backup = form.cleaned_data['time_stamp']
        backup_path = backup.file_path
        directory_name = backup.backupbyowner_set.get(pws_owner=self.request.user).directory_name
        number = form.cleaned_data['pws'].number
        call(["/bin/bash", os.path.join(settings.BASE_DIR, "../download_pws_backup.sh"), backup_path])
        call(["/bin/bash", os.path.join(settings.BASE_DIR, "../restore_backup_pws.sh"), python_path, directory_name,
              number])
        shutil.rmtree('/tmp/backup')
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:backup_pws')
