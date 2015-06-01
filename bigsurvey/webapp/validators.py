import os
from django.core.exceptions import ValidationError
from main.parameters import EXCEL_EXTENSIONS, Messages


def validate_excel_file(file):
    name, ext = os.path.splitext(file.name)
    if ext not in EXCEL_EXTENSIONS:
        raise ValidationError(Messages.extension_not_allowed % {'allowed_extensions': ', '.join(EXCEL_EXTENSIONS)})
