class RenewSessionOnActivity(object):
    def process_request(self, request):
        request.session.set_expiry(request.session.get_expiry_age())
