from .base_views import BaseFormView
from django.views.generic import CreateView, UpdateView
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from webapp import perm_checkers, models, forms
from main.parameters import Messages
import json
from datetime import datetime, timedelta


class TesterCertBaseFormView(BaseFormView):
    form_class = forms.TesterCertForm
    model = models.TesterCert
    template_name = "user/certificate_form.html"

    def get_success_url(self):
        return reverse('webapp:user_detail', args=(self.object.user.pk,))


class TesterCertAddView(TesterCertBaseFormView, CreateView):
    success_message = Messages.TesterCert.tester_cert_add_success
    permission = 'webapp.add_testercert'

    def get_context_data(self, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        if perm_checkers.UserPermChecker.has_perm(self.request, user):
            context = super(TesterCertAddView, self).get_context_data(**kwargs)
            context['user_pk'] = user.pk
            return context
        raise Http404

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['pk'])
        return super(TesterCertAddView, self).form_valid(form)


class TesterCertEditView(TesterCertBaseFormView, UpdateView):
    success_message = Messages.TesterCert.tester_cert_edit_success
    permission = 'webapp.change_testercert'

    def get_form(self, form_class):
        form = super(TesterCertEditView, self).get_form(form_class)
        if perm_checkers.UserPermChecker.has_perm(self.request, form.instance.user):
            return form
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(TesterCertEditView, self).get_context_data(**kwargs)
        context['user_pk'] = context['form'].instance.user.pk
        return context


class TestKitBaseFormView(BaseFormView):
    form_class = forms.TestKitForm
    model = models.TestKit
    template_name = "user/test_kit_form.html"

    def get_success_url(self):
        return reverse('webapp:user_detail', args=(self.object.user.pk,))


class TestKitAddView(TestKitBaseFormView, CreateView):
    success_message = Messages.TestKit.test_kit_add_success
    permission = 'webapp.add_testkit'

    def get_context_data(self, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        if perm_checkers.UserPermChecker.has_perm(self.request, user):
            context = super(TestKitAddView, self).get_context_data(**kwargs)
            context['user_pk'] = user.pk
            return context
        raise Http404

    def form_valid(self, form):
        form.instance.user = User.objects.get(pk=self.kwargs['pk'])
        return super(TestKitAddView, self).form_valid(form)


class TestKitEditView(TestKitBaseFormView, UpdateView):
    success_message = Messages.TestKit.test_kit_edit_success
    permission = 'webapp.change_testkit'

    def get_form(self, form_class):
        form = super(TestKitEditView, self).get_form(form_class)
        if perm_checkers.UserPermChecker.has_perm(self.request, form.instance.user):
            return form
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(TestKitEditView, self).get_context_data(**kwargs)
        context['user_pk'] = context['form'].instance.user.pk
        return context


def get_tester_certs(request, tester_id):
    certs = models.TesterCert.objects.filter(user__pk=tester_id, is_active=True)
    certs_dict = {}
    for cert in certs:
        certs_dict[cert.pk] = cert.cert_number
    return HttpResponse(json.dumps(certs_dict), content_type="application/json")


def get_test_kits(request, tester_id):
    filter_date = datetime.now().date() - timedelta(days=365)
    kits = models.TestKit.objects.filter(user__pk=tester_id, is_active=True, test_last_cert__gte=filter_date)
    kits_dict = {}
    for kit in kits:
        kits_dict[kit.pk] = kit.test_serial
    return HttpResponse(json.dumps(kits_dict), content_type="application/json")
