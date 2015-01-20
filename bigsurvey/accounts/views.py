from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout
from django.views.generic import View
from django.core.urlresolvers import reverse


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm

    def get(self, request):
        form = self.form_class(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return HttpResponseRedirect(reverse('webapp:home'))

        return render(request, self.template_name, {'form': form})