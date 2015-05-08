from main.settings import MEDIA_ROOT, MEDIA_URL
import os
from xhtml2pdf import pisa
from tempfile import TemporaryFile


class PDFGenerator(object):

    @staticmethod
    def generate_letter(letter):
        def media_files_callback(uri, rel):
            return os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ""))
        html = letter.rendered_body
        temp_file = TemporaryFile()
        pisa_status = pisa.CreatePDF(html, temp_file, link_callback=media_files_callback)
        temp_file.seek(0)
        pdf = temp_file.read()
        temp_file.close()
        return pdf