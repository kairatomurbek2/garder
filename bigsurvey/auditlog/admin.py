from django.contrib import admin
from django import forms
from django.forms import Widget
from django.utils.safestring import mark_safe
from reversion.models import Version
from django.utils.translation import ugettext_lazy as _
from diff_match_patch import diff_match_patch

from auditlog.auditlog_helpers import render_diff

dmp = diff_match_patch()


SEMANTIC = 1
EFFICIENCY = 2

Version._meta.verbose_name = _("Reversion")
Version._meta.verbose_name_plural = _("Reversions")


class DateRangeFilter(admin.DateFieldListFilter):
    title = _('Date range')
    template = 'admin/filters/date_range.html'

    def queryset(self, request, queryset):
        if self.used_parameters.has_key(self.lookup_kwarg_since):
            self.start = self.used_parameters[self.lookup_kwarg_since]
        if self.used_parameters.has_key(self.lookup_kwarg_until):
            self.end = self.used_parameters[self.lookup_kwarg_until]
        return super(DateRangeFilter, self).queryset(request, queryset)


class HtmlReadonly(Widget):
    def render(self, name, value, attrs=None):
        current_obj = Version.objects.filter(serialized_data=value)[0]
        html = render_diff(current_obj)
        return mark_safe(html)


class AuditLogForm(forms.ModelForm):
    class Meta:
        model = Version
        widgets = {
            'serialized_data': HtmlReadonly(),
        }
        exclude = []


class AuditLogAdmin(admin.ModelAdmin):
    actions = None
    list_filter = [('revision__date_created', DateRangeFilter), 'content_type']
    search_fields = ['revision__user__username']
    list_display = ['get_date_created', 'get_user', 'content_type', 'get_diff', 'object_id', 'object']
    form = AuditLogForm

    class Meta:
        model = Version

    def get_date_created(self, obj):
        return '%s' % obj.revision.date_created

    get_date_created.short_description = _('Date created')

    def get_user(self, obj):
        return '%s' % obj.revision.user

    get_user.short_description = _('User')

    def get_diff(self, obj):
        return render_diff(obj)

    get_diff.short_description = _("Diff")
    get_diff.allow_tags = True

    # def has_add_permission(self, request):
    #     return False
    def lookup_allowed(self, lookup, value):
        return True

admin.site.register(Version, AuditLogAdmin)
