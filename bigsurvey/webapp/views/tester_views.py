from .base_views import BaseTemplateView, BaseFormView
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from webapp import models, forms, filters
from main.parameters import Messages, Groups
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from smtplib import SMTPException
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class TesterListView(BaseTemplateView):
    template_name = 'user/tester_list.html'
    permission = 'webapp.browse_user'

    def get_context_data(self, **kwargs):
        context = super(TesterListView, self).get_context_data(**kwargs)
        testers = self._get_testers()
        context['tester_filter'] = filters.TesterFilter(self.request.GET, queryset=testers)
        return context

    def _get_testers(self):
        user = self.request.user
        if user.has_perm('webapp.access_to_all_users'):
            return models.User.objects.filter(groups__name=Groups.tester)
        if user.has_perm('webapp.access_to_pws_users'):
            return models.User.objects.filter(groups__name=Groups.tester, employee__pws__in=user.employee.pws.all())


class TesterSearchView(BaseFormView):
    template_name = 'user/tester_search.html'
    form_class = forms.TesterSearchForm
    permission = 'webapp.browse_user'
    tester = None

    def post(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        if form.is_valid():
            valid = self.form_valid(form)
            if 'invite_tester' in request.POST:
                invite_form = forms.TesterInviteForm(queryset=self.request.user.employee.pws.all(), **self.get_form_kwargs())
                if invite_form.is_valid():
                    return self.invite_form_valid(invite_form)
                return self.invite_form_invalid(form, invite_form)
            return valid
        return self.form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        cert_number = form.cleaned_data['cert_number']
        self.tester = self.__get_tester(email, cert_number)
        invite_form = None
        if self.tester:
            if set(self.request.user.employee.pws.all()).issubset(self.tester.employee.pws.all()):
                messages.warning(self.request, Messages.TesterInvite.tester_already_in_pws)
            else:
                invite_form = forms.TesterInviteForm(queryset=self.request.user.employee.pws.all())
        else:
            messages.error(self.request, Messages.TesterInvite.tester_not_found)
        return self.render_to_response({'form': form, 'tester': self.tester, 'invite_form': invite_form})

    def __get_tester(self, email, cert_number):
        if cert_number:
            testers = models.User.objects.filter(
                groups__name=Groups.tester,
                email=email,
                certs__cert_number=cert_number
            )
        else:
            testers = models.User.objects.filter(
                groups__name=Groups.tester,
                email=email,
            )
        if testers:
            return testers.first()
        return None

    def invite_form_valid(self, invite_form):
        invite = models.Invite.objects.create(
            invite_from=self.request.user,
            invite_to=self.tester,
        )
        for pws in invite_form.cleaned_data['pws']:
            invite.invite_pws.add(pws)
        invite.save()
        self.__send_email_to_tester(invite)
        return HttpResponseRedirect(reverse('webapp:tester_list'))

    def __send_email_to_tester(self, invite):
        context = {
            'invite': invite,
            'base_url': settings.HOST
        }
        html_template = 'email_templates/html/pws_invite_notification.html'
        plain_template = 'email_templates/plain/pws_invite_notification.txt'
        subject = 'Invitation from PWS'
        html_content = render_to_string(html_template, context)
        plain_content = render_to_string(plain_template, context)
        try:
            self.tester.email_user(
                subject=subject,
                message=plain_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_message=html_content
            )
            messages.success(self.request, Messages.TesterInvite.tester_invite_success)
        except SMTPException:
            messages.error(self.request, Messages.TesterInvite.tester_invite_failed)

    def invite_form_invalid(self, form, invite_form):
        messages.error(self.request, Messages.TesterInvite.tester_invite_error)
        return self.render_to_response({'form': form, 'tester': self.tester, 'invite_form': invite_form})


class TesterInviteAcceptView(BaseTemplateView):
    template_name = 'user/tester_accept.html'

    def get(self, request, *args, **kwargs):
        try:
            invite = models.Invite.objects.get(code=request.GET.get('code'))
        except ObjectDoesNotExist:
            raise Http404
        if invite.invite_to != request.user:
            raise Http404
        if invite.accepted:
            invite_message = "You have already accepted this invite."
        elif (datetime.now().date() - invite.invite_date).days > 3:
            invite_message = "Invite expired. Please, contact PWS administrator to receive new invite."
        else:
            for pws in invite.invite_pws.all():
                invite.invite_to.employee.pws.add(pws)
            invite.invite_to.employee.save()
            invite.accepted = True
            invite.save()
            invite_message = "Invite successfully accepted."
        self.__send_email_to_admin(invite)
        context = self.get_context_data(**kwargs)
        context['invite_accept_text'] = invite_message
        return self.render_to_response(context)

    def __send_email_to_admin(self, invite):
        context = {
            'invite': invite,
        }
        html_template = 'email_templates/html/pws_invite_accept_notification.html'
        plain_template = 'email_templates/plain/pws_invite_accept_notification.txt'
        subject = 'Invitation have been accepted'
        html_content = render_to_string(html_template, context)
        plain_content = render_to_string(plain_template, context)
        try:
            invite.invite_from.email_user(
                subject=subject,
                message=plain_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_message=html_content
            )
        except SMTPException:
            pass
