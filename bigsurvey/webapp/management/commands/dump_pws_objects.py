from django.core.management.base import BaseCommand
import os
from main.parameters import Groups
from webapp import models
from django.core import serializers
from datetime import datetime
from django.conf import settings
from subprocess import call
import shutil


class Command(BaseCommand):
    help = ('Dump pws objects from the database into JSON that you can'
            'use in a folder and file')

    def handle(self, *args, **options):
        pws_owners = models.User.objects.filter(groups__name=Groups.pws_owner)
        current_date = datetime.now().strftime('%Y-%m-%d-%s')
        for pws_owner in pws_owners:
            pwss = pws_owner.employee.pws.filter(is_active=True)
            path = "/tmp/backup"
            try:
                os.makedirs(path, 0755)
            except OSError as e:
                if e.errno == 17:
                    os.chmod(path, 0755)
            owner_dirname = os.path.join('/tmp/backup/',
                                         pws_owner.username + "_" + current_date)
            os.mkdir(owner_dirname)
            for pws in pwss:
                self.pws_dirname = os.path.join(owner_dirname, pws.number)
                os.mkdir(self.pws_dirname)
                self.dump_by_n(pwss.filter(pk=pws.pk), "pws")
                self.dump_by_n(models.User.objects.filter(employee__pws=pws), "users")
                self.dump_by_n(models.Employee.objects.filter(pws=pws), "employees")
                self.dump_by_n(models.TestKit.objects.filter(user__employee__pws=pws), "test_kit")
                self.dump_by_n(models.TesterCert.objects.filter(user__employee__pws=pws), "test_cert")
                self.dump_by_n(models.ImportLog.objects.filter(pws=pws), "import_log")
                self.dump_by_n(models.LetterType.objects.filter(pws=pws), "letter_type")
                self.dump_by_n(models.Site.objects.filter(pws=pws), "sites")
                self.dump_by_n(models.Hazard.objects.filter(site__pws=pws), "hazards")
                self.dump_by_n(models.Survey.objects.filter(site__pws=pws), "surveys")
                self.dump_by_n(models.BPDevice.objects.filter(hazard__site__pws=pws), "bp_devices")
                self.dump_by_n(models.Test.objects.filter(bp_device__hazard__site__pws=pws), "tests")

        def create_tar(tarname, compress_path, tar_put_path):
            command = 'tar zcf %s/%s -C %s .' % (tar_put_path, tarname, compress_path)
            os.system(command)

        archive_name = "backup_pws_%s.tar.gz" % current_date
        remote_path = os.path.join(settings.BACKUPS_DIR_PWS, archive_name)
        backups_dir = '/tmp/backup'
        create_tar(tarname=archive_name, compress_path=backups_dir, tar_put_path='/tmp')
        call(["/bin/bash", os.path.join(settings.BASE_DIR, "../upload_pws_backup.sh"), archive_name, remote_path])
        backup = models.Backup.objects.create(file_path=remote_path)
        for pws_owner in pws_owners:
            models.BackupByOwner.objects.create(pws_owner=pws_owner, archive_backup=backup,
                                                directory_name=pws_owner.username + "_" + current_date)

        os.remove('/tmp/%s' % archive_name)
        shutil.rmtree('/tmp/backup')

    def dump_by_n(self, queryset, base_filename, n=5000):
        filename = os.path.join(self.pws_dirname, base_filename)
        file_number = 0
        start_id = 0
        end_id = n
        queryset_to_dump = queryset[start_id:end_id]
        while queryset_to_dump.count() > 0:
            out = open("%s_%s.json" % (filename, file_number), "w")
            out.write(serializers.serialize("json", queryset_to_dump))
            out.close()
            start_id = end_id
            end_id = end_id + n
            file_number += 1
            queryset_to_dump = queryset[start_id:end_id]
