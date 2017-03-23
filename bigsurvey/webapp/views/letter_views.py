from .base_views import BaseTemplateView, BaseFormView, BaseView
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from webapp import models, forms, filters, perm_checkers
from webapp.utils.letter_renderer import LetterRenderer
from main.parameters import Messages, Groups
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from smtplib import SMTPException
from django.views.generic import UpdateView, CreateView, FormView
from webapp.responses import PDFResponse
from webapp.utils.pdf_generator import PDFGenerator
from django.core.mail import EmailMessage


class LetterTypeListView(BaseTemplateView):
    template_name = "letter_type/letter_type_list.html"
    permission = 'webapp.browse_lettertype'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LetterTypeListView, self).get_context_data(**kwargs)
        lettertypes = self._get_lettertypes(user)
        context['letter_type_list'] = lettertypes
        return context

    def _get_lettertypes(self, user):
        if user.has_perm('webapp.access_to_all_lettertypes'):
            return models.LetterType.objects.all().order_by('pws')
        if user.has_perm('webapp.access_to_pws_lettertypes'):
            return models.LetterType.objects.filter(pws__in=user.employee.pws.all()).order_by('pws')
        return models.LetterType.objects.none()


class LetterTypeBaseFormView(BaseFormView):
    template_name = "letter_type/letter_type_form.html"
    form_class = forms.LetterTypeForm
    model = models.LetterType

    def get_success_url(self):
        return reverse('webapp:letter_type_list')


class LetterTypeEditView(LetterTypeBaseFormView, UpdateView):
    permission = "webapp.change_lettertype"
    success_message = Messages.LetterType.editing_success
    error_message = Messages.LetterType.editing_error

    def get_form(self, form_class):
        form = super(LetterTypeBaseFormView, self).get_form(form_class)
        if not perm_checkers.LetterTypePermChecker.has_perm(self.request, form.instance):
            raise Http404
        return form

    def get_context_data(self, **kwargs):
        context = super(LetterTypeEditView, self).get_context_data(**kwargs)
        return context


class LetterListView(BaseTemplateView):
    template_name = "letter/letter_list.html"
    permission = 'webapp.browse_letter'

    def get_context_data(self, **kwargs):
        context = super(LetterListView, self).get_context_data(**kwargs)
        letter_filter = filters.LetterFilter(self.request.GET, queryset=self._get_letter_list(), user=self.request.user)
        context['letter_filter'] = letter_filter
        return context

    def _get_letter_list(self):
        if self.request.user.has_perm('webapp.full_letter_access'):
            return models.Letter.objects.all().order_by('-pk')
        elif self.request.user.has_perm('webapp.pws_letter_access'):
            return models.Letter.objects.order_by('-pk').filter(site__pws__in=self.request.user.employee.pws.all())
        else:
            raise Http404


class LetterBaseFormView(BaseFormView):
    template_name = "letter/letter_form.html"
    form_class = forms.LetterForm
    model = models.Letter

    def get_success_url(self):
        return reverse("webapp:letter_detail", args=(self.object.pk,))

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(LetterBaseFormView, self).form_valid(form)
        LetterRenderer.render(self.object)
        return response


class LetterAddView(LetterBaseFormView, CreateView):
    permission = "webapp.send_letter"
    success_message = Messages.Letter.adding_success
    error_message = Messages.Letter.adding_error

    def get_form(self, form_class):
        site = models.Site.active_only.get(pk=self.kwargs['pk'])
        if perm_checkers.SitePermChecker.has_perm(self.request, site):
            form = super(LetterAddView, self).get_form(form_class)
            form.fields['hazard'].queryset = site.hazards.filter(is_present=True)
            form.fields['letter_type'].queryset = site.pws.letter_types
            return form
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(LetterAddView, self).get_context_data(**kwargs)
        context['site'] = models.Site.active_only.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.site = models.Site.active_only.get(pk=self.kwargs['pk'])
        return super(LetterAddView, self).form_valid(form)


class LetterEditView(LetterBaseFormView, UpdateView):
    permission = "webapp.send_letter"
    success_message = Messages.Letter.editing_success
    error_message = Messages.Letter.editing_error

    def get_form(self, form_class):
        form = super(LetterEditView, self).get_form(form_class)
        if perm_checkers.LetterPermChecker.has_perm(self.request, form.instance):
            site = form.instance.site
            form.fields['hazard'].queryset = site.hazards.filter(is_present=True)
            form.fields['letter_type'].queryset = site.pws.letter_types
            return form
        raise Http404

    def get_context_data(self, **kwargs):
        context = super(LetterEditView, self).get_context_data(**kwargs)
        context['site'] = context['form'].instance.site
        return context


class LetterMixin(object):
    def get_email_body(self, letter, form, is_pdf=False):
        html = letter.rendered_body

        new_page_inserted = False
        page_delimiter = '<pdf:nextpage />'
        if form.cleaned_data.get('attach_testers', False):
            testers_true = models.User.objects.filter(groups__name=Groups.tester, employee__pws=letter.site.pws,
                                                      employee__has_licence_for_installation=True)
            testers_false = models.User.objects.filter(groups__name=Groups.tester, employee__pws=letter.site.pws,
                                                       employee__has_licence_for_installation=False)
            if is_pdf:
                html += '<pdf:nexttemplate name="testers" />'
                html += page_delimiter
                new_page_inserted = True
            html += render_to_string('email_templates/html/testers_list.html',
                                     {'testers_true': testers_true, 'testers_false': testers_false})
        if form.cleaned_data.get('attach_consultant_info', False):
            if is_pdf and not new_page_inserted:
                html += page_delimiter
            html += render_to_string('email_templates/html/consultant_info.html', {'pws': letter.site.pws})
        return html


class LetterDetailView(BaseTemplateView, FormView, LetterMixin):
    template_name = "letter/letter_detail.html"
    permission = 'webapp.browse_letter'
    form_class = forms.LetterSendForm
    success_url = 'webapp:letter_list'
    success_message = Messages.Letter.send_success
    error_message = Messages.Letter.send_error

    def get_context_data(self, **kwargs):
        letter = models.Letter.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.LetterPermChecker.has_perm(self.request, letter):
            raise Http404
        self._set_messages(letter)
        context = super(LetterDetailView, self).get_context_data(**kwargs)
        context['letter'] = letter
        context['form'] = self.form_class(initial={'send_to': letter.site.contact_email})
        return context

    def _set_messages(self, letter):
        if not letter.already_sent:
            warnings = LetterRenderer.render(letter)
            if warnings:
                messages.warning(self.request, Messages.Letter.fields_without_value % ", ".join(warnings))
            else:
                messages.success(self.request, Messages.Letter.required_data_present)
        else:
            messages.info(self.request, Messages.Letter.letter_already_sent)

    def form_valid(self, form):
        letter = models.Letter.objects.get(pk=self.kwargs['pk'])
        self._send_email(letter, form)
        return HttpResponseRedirect(reverse(self.success_url))

    def _send_email(self, letter, form):
        body = self.get_email_body(letter, form)

        msg = EmailMessage(
            letter.letter_type.header,
            body,
            to=map(lambda email: email.strip(), form.cleaned_data['send_to'].strip(', ').split(',')),
            headers={'From': settings.DEFAULT_FROM_EMAIL, 'Reply-To': settings.REPLY_TO_EMAIL, 'Return-Path': settings.RETURN_PATH_EMAIL}
        )
        msg.content_subtype = 'html'
        try:
            msg.send()
            messages.success(self.request, self.success_message)
            letter.already_sent = True
            letter.save()
        except SMTPException:
            messages.error(self.request, self.error_message)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super(LetterDetailView, self).form_invalid(form)


class LetterPDFView(BaseView, FormView, LetterMixin):
    template_name = "letter/letter_pdf_options_modal.html"
    permission = 'webapp.send_letter'
    form_class = forms.LetterOptionsForm

    def get_context_data(self, **kwargs):
        context = super(LetterPDFView, self).get_context_data(**kwargs)
        context['letter'] = models.Letter.objects.get(pk=self.kwargs['pk'])
        return context

    def append_styles(self):
        styles = render_to_string('partial/pdf_styles.html')
        return styles

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            letter = models.Letter.objects.get(pk=self.kwargs['pk'])

            body = self.get_email_body(letter, form, is_pdf=True)
            letter.already_sent = True
            letter.save()
            body += self.append_styles()
            pdf_content = PDFGenerator.generate_from_html(body)
            filename = u"%s_%s_%s.pdf" % (letter.date, letter.letter_type.letter_type.replace(' ', '_'), letter.site.cust_number)
            return PDFResponse(filename=filename, content=pdf_content)
