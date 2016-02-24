import subprocess
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.views.generic import FormView
import os
from webapp.forms import BackupForm
from django.conf import settings


class BackupsView(FormView):
    template_name = "admin/backups.html"
    form_class = BackupForm
    success_url = reverse_lazy('admin:backups')

    def form_valid(self, form):
        filename = form.cleaned_data['backup']
        response = super(BackupsView, self).form_valid(form)
        if "_restore" in self.request.POST:
            subprocess.call(
                [settings.RESTORE_BACKUP_SCRIPT, settings.DATABASES['default']['NAME'],
                 settings.DATABASES['default']['USER'],
                 settings.DATABASES['default']['PASSWORD'], os.path.join(settings.BASE_DIR, '..'), filename])
            return response
        elif "_create" in self.request.POST:
            subprocess.call([settings.CREATE_BACKUP_SCRIPT, settings.DATABASES['default']['NAME'],
                             settings.DATABASES['default']['USER'],
                             settings.DATABASES['default']['PASSWORD'], os.path.join(settings.BASE_DIR, '..')])
            return response
        elif "_latest" in self.request.POST:
            subprocess.call([settings.RESTORE_BACKUP_SCRIPT, settings.DATABASES['default']['NAME'],
                             settings.DATABASES['default']['USER'],
                             settings.DATABASES['default']['PASSWORD'], os.path.join(settings.BASE_DIR, '..')])
            return response
        elif "_upload" in self.request.POST:
            backup = self.request.FILES.get('upload_backup')
            if backup:
                destination = open(os.path.join(settings.BACKUPS_DIR, 'uploaded.tar.gz'), 'wb+')
                for chunk in backup.chunks():
                    destination.write(chunk)
                destination.close()
            return response
        else:
            file_path = os.path.join(settings.BACKUPS_DIR, filename)
            wrapper = FileWrapper(file(file_path))
            response = HttpResponse(wrapper, content_type='application/x-gzip')
            response['Content-Disposition'] = 'attachment; filename="%s"' % form.cleaned_data['backup']
            response['Content-Length'] = os.path.getsize(file_path)
            return response
