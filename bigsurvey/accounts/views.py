from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.views.generic import View
from django.core.urlresolvers import reverse

from main.parameters import Groups


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def get(self, request):
        if self.request.user.is_authenticated():
            if request.user.groups.filter(name=Groups.ad_auth):
                return HttpResponseRedirect(reverse('webapp:pws_list'))
            return HttpResponseRedirect(request.GET.get('next', reverse('webapp:home')))
        form = self.form_class(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.user.groups.filter(name=Groups.ad_auth):
                return HttpResponseRedirect(reverse('webapp:pws_list'))
            return HttpResponseRedirect(request.GET.get('next', reverse('webapp:home')))
        return render(request, self.template_name, {'form': form})