from ajax_select import register, LookupChannel
from models import Site
from django.db.models import Q
@register('site')
class SiteLookup(LookupChannel):

    model = Site

    def get_query(self, q, request):
        return self.model.objects.filter(Q(street_number__icontains=q)|Q(address1__icontains=q)|Q(city__icontains=q)|Q(zip__icontains=q)).order_by('city')[:50]

    def format_item_display(self, item):
        return u"<span class='tag'>%s</span>" % item
