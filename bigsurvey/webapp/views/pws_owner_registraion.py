from django.conf import settings
from django.contrib.auth.models import Group
from django.core.mail.message import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.views.generic import FormView, View
from main.parameters import PWSRegistrationEmail, Messages, Groups
import os
from webapp import models
from webapp.actions.builders import SampleSitesJsonUploaderBuilder
from webapp.actions.demo_trial import DemoTrialCreator
from webapp.forms import PWSOwnerRegistrationForm, PWSUserAddForm
from django.contrib import messages
from django.core.urlresolvers import reverse


class PwsOwnerRegistrationView(FormView):
    template_name = 'pws_owner_registration/pws_owner_registration.html'
    msg_content_template_email = 'pws_owner_registration/pws_name_mail.html'
    success_message = Messages.PWS.adding_success_trial_demo

    def get_success_url(self):
        return reverse('webapp:pws_owner_registration')

    def get(self, request, *args, **kwargs):
        pws_form = PWSOwnerRegistrationForm()
        pws_form.prefix = 'pws_form'
        user_form = PWSUserAddForm()
        user_form.prefix = 'user_form'
        return self.render_to_response(self.get_context_data(pws_form=pws_form, user_form=user_form))

    def post(self, request, *args, **kwargs):
        pws_form = PWSOwnerRegistrationForm(self.request.POST, prefix='pws_form')
        user_form = PWSUserAddForm(self.request.POST, prefix='user_form')

        if pws_form.is_valid() and user_form.is_valid():
            pws = self._create_pws(pws_form)
            employee = self._create_user_and_employee(user_form, pws)
            email = employee.user.email
            self.send_email(request, email, pws, employee.user)
            test_pws = self._create_test_pws()
            self.upload_sample_sites(test_pws)
            employee.pws.add(test_pws)
            employee.save()
            self.create_demo_trial(employee)
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(pws_form, user_form, **kwargs)

    def form_invalid(self, pws_form, user_form, **kwargs):
        pws_form.prefix = 'pws_form'
        user_form.prefix = 'user_form'
        return self.render_to_response(self.get_context_data(pws_form=pws_form, user_form=user_form))

    @staticmethod
    def _create_pws(pws_form):
        number = pws_form.cleaned_data['number']
        name = pws_form.cleaned_data['name']
        county = pws_form.cleaned_data['county']
        office_address = pws_form.cleaned_data['office_address']
        city = pws_form.cleaned_data['city']
        state = pws_form.cleaned_data['state']
        zip = pws_form.cleaned_data['zip']
        phone = pws_form.cleaned_data['phone']
        pws = models.PWS.objects.create(number=number, name=name, county=county, office_address=office_address,
                                        city=city, state=state, zip=zip, phone=phone)
        return pws

    @staticmethod
    def _create_test_pws():
        number = Messages.PWS.test_pws_number
        name = Messages.PWS.test_pws_name
        county = 'Sample'
        pws = models.PWS.objects.create(number=number, name=name, county=county)
        return pws

    @staticmethod
    def _create_user_and_employee(user_form, pws):
        password = user_form.cleaned_data['password1']
        user = user_form.save()
        user.set_password(password)
        user.groups.add(Group.objects.get(name=Groups.pws_owner))
        employee = models.Employee.objects.create(user=user)
        employee.pws.add(pws)
        return employee

    def send_email(self, request, email, pws, user):
        subject = PWSRegistrationEmail.successfull_registration_subject % pws.name
        context_email = RequestContext(request,
                                       {'pws': pws, 'username': user.username, 'site_url': self.request.get_host()})
        message_html = loader.get_template(self.msg_content_template_email).render(context_email)
        msg = EmailMultiAlternatives(subject=subject, body=message_html,
                                     headers={'Reply-To': settings.PWS_REGISTATION_FROM_EMAIL},
                                     to=[email])
        file_name_pdf = models.TermsConditions.objects.all().first().pdf_file
        file_name_xlsx = 'Sample_Town.xlsx'
        msg.attach_alternative(message_html, "text/html")
        msg.attach_file(os.path.join(settings.MEDIA_ROOT, file_name_pdf.name), "application/pdf")
        msg.attach_file(os.path.join(settings.MEDIA, file_name_xlsx), "application/xlsx")
        msg.send()

    @staticmethod
    def upload_sample_sites(pws):
        action = SampleSitesJsonUploaderBuilder.load_sample_data(pws)
        action.execute()

    @staticmethod
    def create_demo_trial(employee):
        demo_trial_creator = DemoTrialCreator()
        demo_trial_creator.employee = employee
        demo_trial_creator.create_demo_trial_for_user()


class DownloadPublishedQuiz(View):
    @staticmethod
    def get(*args, **kwargs):
        file = models.TermsConditions.objects.all().first().pdf_file
        response = HttpResponse(file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file.name)
        return response
