from django.conf.urls import patterns, url
from webapp.backup_views import BackupsView
from django.contrib.admin import AdminSite, sites
from django.contrib.auth.admin import Group, GroupAdmin, User, UserAdmin


class AdminSiteBigsurvey(AdminSite):
    def get_urls(self):
        urls = super(AdminSiteBigsurvey, self).get_urls()
        my_urls = patterns(
            '',
            url(r'^backups/$', self.admin_view(BackupsView.as_view()), name='backups')
        )
        return my_urls + urls


admin_site_bigsurvey = AdminSiteBigsurvey()
sites.site = admin_site_bigsurvey
admin_site_bigsurvey.register(User, UserAdmin)
admin_site_bigsurvey.register(Group, GroupAdmin)
