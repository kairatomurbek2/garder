from datetime import datetime, timedelta
from django.conf import settings
from django.core.management import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        self._clean_dir(settings.EXCEL_EXPORT_DIR)
        self._clean_dir(settings.EXCEL_FILES_DIR)

    def _clean_dir(self, dir):
        deadline = datetime.now() - timedelta(days=settings.DELETE_OLD_XLS_FILES_AFTER_DAYS)
        for file in os.listdir(dir):
            if file.endswith('xlsx') or file.endswith('xls'):
                file_path = os.path.join(dir, file)
                file_last_modify = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_last_modify < deadline:
                    os.remove(file_path)
