

class SitesFilteringFormNotProvidedException(Exception):
    pass


class FilterSitesAction(object):
    sites_filtering_form = None
    pws_list = None
    sites = None

    def execute(self):
        if not self.sites_filtering_form:
            raise SitesFilteringFormNotProvidedException()
        sites = self._filter_sites(self.sites_filtering_form)
        return sites

    def _filter_sites(self, form):
        kwargs = self._prepare_kwargs(form)
        if kwargs['pws']:
            pws_list = [kwargs['pws']]
        else:
            pws_list = self.pws_list
        sites = self.sites.filter(pws__in=pws_list)
        if kwargs.get('cust_number', None):
            sites = sites.filter(cust_number__icontains=kwargs['cust_number'])
        if kwargs.get('cust_code', None):
            sites = sites.filter(cust_code=kwargs['cust_code'])
        if kwargs.get('cust_name', None):
            sites = sites.filter(cust_name__icontains=kwargs['cust_name'])
        if kwargs.get('street_number', None):
            sites = sites.filter(street_number__icontains=kwargs['street_number'])
        if kwargs.get('address1', None):
            sites = sites.filter(address1__icontains=kwargs['address1'])
        if kwargs.get('address2', None):
            sites = sites.filter(address2__icontains=kwargs['address2'])
        if kwargs.get('apt', None):
            sites = sites.filter(apt__icontains=kwargs['apt'])
        if kwargs.get('city', None):
            sites = sites.filter(city__icontains=kwargs['city'])
        if kwargs.get('state', None):
            val = kwargs['state']
            if val == 'blank':
                sites = sites.filter(state=None)
            else:
                sites = sites.filter(state=val)
        if kwargs.get('zip', None):
            sites = sites.filter(zip__icontains=kwargs['zip'])
        if kwargs.get('cust_address1', None):
            sites = sites.filter(cust_address1__icontains=kwargs['cust_address1'])
        if kwargs.get('cust_address2', None):
            sites = sites.filter(cust_address2__icontains=kwargs['cust_address2'])
        if kwargs.get('cust_apt', None):
            sites = sites.filter(cust_apt__icontains=kwargs['cust_apt'])
        if kwargs.get('cust_city', None):
            sites = sites.filter(cust_city__icontains=kwargs['cust_city'])
        if kwargs.get('cust_state', None):
            val = kwargs['cust_state']
            if val == 'blank':
                sites = sites.filter(cust_state=None)
            else:
                sites = sites.filter(cust_state=val)
        if kwargs.get('cust_zip', None):
            sites = sites.filter(cust_zip__icontains=kwargs['cust_zip'])
        if kwargs.get('next_survey_from', None):
            sites = sites.filter(next_survey_date__gte=kwargs['next_survey_from'])
        if kwargs.get('next_survey_to', None):
            sites = sites.filter(next_survey_date__lte=kwargs['next_survey_to'])
        if kwargs.get('next_survey_blank', None):
            sites = sites.filter(next_survey_date__isnull=True)
        if kwargs.get('last_survey_from', None):
            sites = sites.filter(last_survey_date__gte=kwargs['last_survey_from'])
        if kwargs.get('last_survey_to', None):
            sites = sites.filter(last_survey_date__lte=kwargs['last_survey_to'])
        if kwargs.get('last_survey_blank', None):
            sites = sites.filter(last_survey_date__isnull=True)
        if kwargs.get('due_test_from', None):
            sites = sites.filter(due_install_test_date__gte=kwargs['due_test_from'])
        if kwargs.get('due_test_to', None):
            sites = sites.filter(due_install_test_date__lte=kwargs['due_test_to'])
        if kwargs.get('due_test_blank', None):
            sites = sites.filter(due_install_test_date__isnull=True)
        if kwargs.get('route', None):
            sites = sites.filter(route__icontains=kwargs['route'])
        if kwargs.get('meter_number', None):
            sites = sites.filter(meter_number__icontains=kwargs['meter_number'])
        if kwargs.get('meter_size', None):
            sites = sites.filter(meter_size__icontains=kwargs['meter_size'])
        if kwargs.get('meter_reading', None):
            sites = sites.filter(meter_reading__icontains=kwargs['meter_reading'])
        if kwargs.get('connect_date_from', None):
            sites = sites.filter(connect_date__gte=kwargs['connect_date_from'])
        if kwargs.get('connect_date_to', None):
            sites = sites.filter(connect_date__lte=kwargs['connect_date_to'])
        if kwargs.get('street_number_blank', None):
            sites = sites.filter(street_number__isnull=True) | sites.filter(street_number='')
        if kwargs.get('address2_blank', None):
            sites = sites.filter(address2__isnull=True) | sites.filter(address2='')
        if kwargs.get('apt_blank', None):
            sites = sites.filter(apt__isnull=True) | sites.filter(apt='')
        if kwargs.get('zip_blank', None):
            sites = sites.filter(zip__isnull=True) | sites.filter(zip='')
        if kwargs.get('cust_address1_blank', None):
            sites = sites.filter(cust_address1__isnull=True) | sites.filter(cust_address1='')
        if kwargs.get('cust_address2_blank', None):
            sites = sites.filter(cust_address2__isnull=True) | sites.filter(cust_address2='')
        if kwargs.get('cust_apt_blank', None):
            sites = sites.filter(cust_apt__isnull=True) | sites.filter(cust_apt='')
        if kwargs.get('cust_city_blank', None):
            sites = sites.filter(cust_city__isnull=True) | sites.filter(cust_city='')
        if kwargs.get('cust_zip_blank', None):
            sites = sites.filter(cust_zip__isnull=True) | sites.filter(cust_zip='')
        if kwargs.get('route_blank', None):
            sites = sites.filter(route__isnull=True) | sites.filter(route='')
        if kwargs.get('meter_number_blank', None):
            sites = sites.filter(meter_number__isnull=True) | sites.filter(meter_number='')
        if kwargs.get('meter_size_blank', None):
            sites = sites.filter(meter_size__isnull=True) | sites.filter(meter_size='')
        if kwargs.get('meter_reading_blank', None):
            sites = sites.filter(meter_reading__isnull=True)
        if kwargs.get('connect_date_blank', None):
            sites = sites.filter(connect_date__isnull=True)
        return sites

    def _prepare_kwargs(self, form):
        kwargs = {}
        try:
            kwargs['pws'] = form.cleaned_data['pws']
            kwargs['due_test_from'] = form.cleaned_data['due_test_from']
            kwargs['due_test_to'] = form.cleaned_data['due_test_to']
            kwargs['next_survey_from'] = form.cleaned_data['next_survey_from']
            kwargs['next_survey_to'] = form.cleaned_data['next_survey_to']
            kwargs['last_survey_from'] = form.cleaned_data['last_survey_from']
            kwargs['last_survey_to'] = form.cleaned_data['last_survey_to']
            kwargs['connect_date_from'] = form.cleaned_data['connect_date_from']
            kwargs['connect_date_to'] = form.cleaned_data['connect_date_to']
            kwargs['due_test_blank'] = form.cleaned_data['due_test_blank']
            kwargs['next_survey_blank'] = form.cleaned_data['next_survey_blank']
            kwargs['last_survey_blank'] = form.cleaned_data['last_survey_blank']
            kwargs['route_blank'] = form.cleaned_data['route_blank']
            kwargs['street_number_blank'] = form.cleaned_data['street_number_blank']
            kwargs['address2_blank'] = form.cleaned_data['address2_blank']
            kwargs['cust_address2_blank'] = form.cleaned_data['cust_address2_blank']
            kwargs['apt_blank'] = form.cleaned_data['apt_blank']
            kwargs['zip_blank'] = form.cleaned_data['zip_blank']
            kwargs['cust_address1_blank'] = form.cleaned_data['cust_address1_blank']
            kwargs['cust_apt_blank'] = form.cleaned_data['cust_apt_blank']
            kwargs['cust_city_blank'] = form.cleaned_data['cust_city_blank']
            kwargs['cust_zip_blank'] = form.cleaned_data['cust_zip_blank']
            kwargs['meter_number_blank'] = form.cleaned_data['meter_number_blank']
            kwargs['meter_size_blank'] = form.cleaned_data['meter_size_blank']
            kwargs['meter_reading_blank'] = form.cleaned_data['meter_reading_blank']
            kwargs['connect_date_blank'] = form.cleaned_data['connect_date_blank']
            kwargs['cust_number'] = form.cleaned_data['cust_number']
            kwargs['cust_code'] = form.cleaned_data['cust_code']
            kwargs['street_number'] = form.cleaned_data['street_number']
            kwargs['address1'] = form.cleaned_data['address1']
            kwargs['address2'] = form.cleaned_data['address2']
            kwargs['apt'] = form.cleaned_data['apt']
            kwargs['city'] = form.cleaned_data['city']
            kwargs['state'] = form.cleaned_data['state']
            kwargs['zip'] = form.cleaned_data['zip']
            kwargs['cust_address1'] = form.cleaned_data['cust_address1']
            kwargs['cust_address2'] = form.cleaned_data['cust_address2']
            kwargs['cust_apt'] = form.cleaned_data['cust_apt']
            kwargs['cust_city'] = form.cleaned_data['cust_city']
            kwargs['route'] = form.cleaned_data['route']
            kwargs['meter_number'] = form.cleaned_data['meter_number']
            kwargs['meter_size'] = form.cleaned_data['meter_size']
            kwargs['meter_reading'] = form.cleaned_data['meter_reading']
            kwargs['cust_name'] = form.cleaned_data['cust_name']
            kwargs['cust_zip'] = form.cleaned_data['cust_zip']
            kwargs['cust_state'] = form.cleaned_data['cust_state']
        except AttributeError:
            kwargs['pws'] = self.pws_list
        except TypeError:
            kwargs['pws'] = self.pws_list
        return kwargs
