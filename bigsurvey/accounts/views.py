from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import login as auth_login, logout, REDIRECT_FIELD_NAME


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url('/')
            auth_login(request, form.get_user())
            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)
    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app, )