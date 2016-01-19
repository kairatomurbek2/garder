from django.views.generic import CreateView, UpdateView
from .base_views import BaseTemplateView, BaseFormView


class BPDeviceListView(BaseTemplateView):
    pass


class BPDeviceDetailView(BaseTemplateView):
    pass


class BPDeviceCreateView(BaseFormView, CreateView):
    pass


class BPDeviceUpdateView(BaseFormView, UpdateView):
    pass
