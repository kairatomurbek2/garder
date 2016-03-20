from django.conf import settings


def use_captcha(request):
    return {'use_captcha_template': settings.USE_CAPTHCA}
