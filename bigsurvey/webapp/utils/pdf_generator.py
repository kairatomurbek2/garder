import StringIO
import os
import urllib

from xhtml2pdf import pisa

from main.settings import MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL


class PDFGenerator(object):
    @staticmethod
    def generate_from_html(html):
        stream = StringIO.StringIO()
        pisa.CreatePDF(html, stream)
        return stream.getvalue()