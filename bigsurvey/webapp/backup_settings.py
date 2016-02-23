import subprocess
from django.conf import settings

subprocess.call(
    [settings.CREATE_BACKUP_SCRIPT, settings.DATABASES['default']['NAME'], settings.DATABASES['default']['USER'],
     settings.DATABASES['default']['PASSWORD']])

subprocess.call(
    [settings.RESTORE_BACKUP_SCRIPT, settings.DATABASES['default']['NAME'], settings.DATABASES['default']['USER'],
     settings.DATABASES['default']['PASSWORD']])
