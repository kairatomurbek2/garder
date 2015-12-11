import StringIO
from xhtml2pdf import pisa
import os


class PDFGenerator(object):
    @staticmethod
    def generate_from_html(html):
        stream = StringIO.StringIO()
        pisa.CreatePDF(html, stream)
        return stream.getvalue()

