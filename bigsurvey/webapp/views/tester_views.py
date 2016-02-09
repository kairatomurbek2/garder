from .base_views import BaseTemplateView
from webapp import models, filters
from main.parameters import Groups


class TesterListView(BaseTemplateView):
    template_name = 'user/tester_list.html'
    permission = 'webapp.browse_user'

    def get_context_data(self, **kwargs):
        context = super(TesterListView, self).get_context_data(**kwargs)
        testers = self._get_testers()
        context['tester_filter'] = filters.TesterFilter(self.request.GET, queryset=testers, user=self.request.user)
        return context

    def _get_testers(self):
        user = self.request.user
        if user.has_perm('webapp.access_to_all_users'):
            return models.User.objects.filter(groups__name=Groups.tester)
        if user.has_perm('webapp.access_to_pws_users'):
            return models.User.objects.filter(groups__name=Groups.tester, employee__pws__in=user.employee.pws.all())
