from ajax_select import register, LookupChannel
from models import Site,Hazard
from django.db.models import Q
@register('site')
class SiteLookup(LookupChannel):

    model = Site

    def get_query(self, q, request):
        return self.model.objects.filter(Q(street_number__icontains=q)|Q(address1__icontains=q)|Q(city__icontains=q)|Q(zip__icontains=q)).order_by('city')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item

@register('hazard')
class HazardLookup(LookupChannel):

    model = Hazard

    def get_query(self, q, request):
        return self.model.objects.filter(Q(hazard_type__icontains=q)|Q(service_type__icontains=q)|Q(site__cust_number__icontains=q)).order_by('id')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item
