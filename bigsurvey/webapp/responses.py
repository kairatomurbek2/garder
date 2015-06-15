from django.http import HttpResponse


class PDFResponse(HttpResponse):
    def __init__(self, filename, *args, **kwargs):
        super(PDFResponse, self).__init__(content_type='application/pdf', *args, **kwargs)
        self['Content-Disposition'] = u'attachment; filename="%s"' % filename