from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from .base_views import BaseFormView
from main.parameters import AssemblyStatus
from webapp.models import BPDevice, Hazard
from webapp.forms import BPForm


class BPDeviceBaseFormView(BaseFormView):
    template_name = "bp_device/bp_device_form.html"
    form_class = BPForm
    model = BPDevice

    def get_context_data(self, **kwargs):
        user = self.request.user
        if user.has_perm("webapp.change_hazard") or user.employee.has_licence_for_installation:
            return super(BPDeviceBaseFormView, self).get_context_data(**kwargs)
        raise Http404

    def get_success_url(self):
        return reverse('webapp:hazard_detail', args=(self.object.hazard.pk,))


class BPDeviceCreateView(BPDeviceBaseFormView, CreateView):
    permission = 'webapp.add_bpdevice'

    def form_valid(self, form):
        self.object = form.save()
        self._update_hazard(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def _update_hazard(self, bp_device):
        hazard = Hazard.objects.get(pk=self.kwargs['pk'])
        hazard.bp_device = bp_device
        hazard.assembly_status = AssemblyStatus.INSTALLED
        hazard.save()

    def get_context_data(self, **kwargs):
        context = super(BPDeviceCreateView, self).get_context_data(**kwargs)
        if self.allowed():
            context['hazard_pk'] = self.kwargs['pk']
            return context
        raise Http404

    def allowed(self):
        hazard = Hazard.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        return user.has_perm('webapp.access_to_all_devices') or\
               hazard.site.pws in user.employee.pws.all() and user.has_perm('webapp.access_to_pws_devices')


# actually never used
class BPDeviceUpdateView(BPDeviceBaseFormView, UpdateView):
    permission = 'webapp.change_bpdevice'

    def get_context_data(self, **kwargs):
        context = super(BPDeviceUpdateView, self).get_context_data(**kwargs)
        hazard = context['form'].instance.hazard
        if self.allowed(hazard):
            return context
        raise Http404

    def allowed(self, hazard):
        user = self.request.user
        return user.has_perm('webapp.access_to_all_devices') or\
               hazard.site.pws in user.employee.pws.all() and user.has_perm('webapp.access_to_pws_devices')
