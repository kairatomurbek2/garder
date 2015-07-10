import StringIO
import os

from xhtml2pdf import pisa

from main.settings import MEDIA_ROOT, MEDIA_URL


class PDFGenerator(object):
    @staticmethod
    def generate_from_html(html):
        def media_files_callback(uri, rel):
            return os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ""))
        stream = StringIO.StringIO()
        pisa.CreatePDF(html, stream, link_callback=media_files_callback)
        return stream.getvalue()