import StringIO
import os
import urllib

from xhtml2pdf import pisa

from main.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL


class PDFGenerator(object):
    @staticmethod
    def generate_from_html(html):
        def media_files_callback(uri, rel):
            uri = urllib.unquote_plus(uri)
            if uri.startswith(STATIC_URL):
                path = os.path.join(STATIC_ROOT, uri.replace(STATIC_URL, ""))
            elif uri.startswith(MEDIA_URL):
                path = os.path.join(MEDIA_ROOT, uri.replace(MEDIA_URL, ""))
            return path

        stream = StringIO.StringIO()
        pisa.CreatePDF(html, stream)
        return stream.getvalue()