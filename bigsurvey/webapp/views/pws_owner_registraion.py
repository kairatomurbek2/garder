from django.contrib.auth.models import Group
from django.core.mail.message import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template import RequestContext, loader
from django.views.generic import FormView
from main.parameters import PWSRegistrationEmail, Messages
from webapp import models
from webapp.actions.builders import SampleSitesJsonUploaderBuilder
from webapp.forms import PWSOwnerRegistrationForm, PWSUserAddForm


class PwsOwnerRegistrationView(FormView):
    template_name = 'pws_owner_registration/pws_owner_registration.html'
    msg_content_template_email = 'pws_owner_registration/pws_name_mail.html'
    success_message = Messages.PWS.adding_success
    error_message = Messages.PWS.adding_error

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
            self.upload_sample_sites(pws)
            return HttpResponseRedirect('/')
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
        pws = models.PWS.objects.create(number=number, name=name)
        return pws

    @staticmethod
    def _create_user_and_employee(user_form, pws):
        address = user_form.cleaned_data['address']
        city = user_form.cleaned_data['city']
        state = user_form.cleaned_data['state']
        zip = user_form.cleaned_data['zip']
        phone1 = user_form.cleaned_data['phone1']
        password = user_form.cleaned_data['password1']
        user = user_form.save()
        user.set_password(password)
        user.groups.add(Group.objects.get(name='PWSOwners'))
        employee = models.Employee.objects.create(address=address, city=city, state=state, zip=zip, phone1=phone1,
                                                  user=user)
        employee.pws.add(pws)
        return employee

    def send_email(self, request, email, pws, user):
        subject = PWSRegistrationEmail.successfull_registration_subject % pws.name
        context_email = RequestContext(request, {'pws': pws, 'username': user.username})
        message_html = loader.get_template(self.msg_content_template_email).render(context_email)
        msg = EmailMultiAlternatives(subject=subject, body=message_html, to=[email])
        msg.attach_alternative(message_html, "text/html")
        msg.send()

    @staticmethod
    def upload_sample_sites(pws):
        action = SampleSitesJsonUploaderBuilder.load_sample_data(pws)
        action.execute()
