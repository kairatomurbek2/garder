import django_filters
import models


class SiteFilter(django_filters.FilterSet):
    customer = django_filters.CharFilter(lookup_type='name__icontains', label='')
    pws = django_filters.CharFilter(label='', lookup_type='name__icontains')
    city = django_filters.CharFilter(lookup_type='icontains', label='')
    address1 = django_filters.CharFilter(lookup_type='icontains', label='')
    site_type = django_filters.CharFilter(label='', lookup_type='site_type__icontains')
    site_use = django_filters.CharFilter(label='', lookup_type='site_use__icontains')

    class Meta:
        models = models.Site
        fields = ['customer', 'pws', 'city', 'address1', 'site_use', 'site_type']