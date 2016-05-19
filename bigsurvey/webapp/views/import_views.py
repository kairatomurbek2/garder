import json
import time

import os
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.db.models import NOT_PROVIDED
from django.forms import formset_factory, ModelChoiceField
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from main.parameters import Messages, OTHER, DATEFORMAT_HELP
from webapp import models, perm_checkers, filters
from webapp.forms import ImportForm, ImportMappingsForm, BaseImportMappingsFormSet
from webapp.utils.excel_parser import ExcelParser, ExcelValidationError, BackgroundExcelParserRunner, FINISHED
from .base_views import BaseTemplateView, BaseFormView


class ImportView(BaseFormView):
    permission = 'webapp.access_to_import'
    template_name = 'import/import.html'
    form_class = ImportForm

    def get_form(self, form_class):
        self._delete_cached_data()
        form = super(ImportView, self).get_form(form_class)
        if self.request.user.has_perm('webapp.access_to_all_sites'):
            form.fields['pws'] = ModelChoiceField(queryset=models.PWS.objects.all())
        elif self.request.user.has_perm('webapp.access_to_multiple_pws_sites'):
            form.fields['pws'] = ModelChoiceField(queryset=self.request.user.employee.pws.all())
        return form

    def get_context_data(self, **kwargs):
        context = super(ImportView, self).get_context_data(**kwargs)
        context['dateformat_help'] = DATEFORMAT_HELP
        return context

    def form_valid(self, form):
        self._delete_previous_tmp_files()
        filename = self._save_tmp_file(form.cleaned_data.get('file'))
        self.request.session['import_filename'] = filename
        if form.cleaned_data.get('date_format') == OTHER:
            self.request.session['import_date_format'] = form.cleaned_data.get('date_format_other')
        else:
            self.request.session['import_date_format'] = form.cleaned_data.get('date_format')
        try:
            self.request.session['import_pws_pk'] = form.cleaned_data['pws'].pk
        except KeyError:
            self.request.session['import_pws_pk'] = self.request.user.employee.pws.all()[0].pk
        self.request.session['import_update_only'] = form.cleaned_data.get('update_only')
        return super(ImportView, self).form_valid(form)

    def _delete_previous_tmp_files(self):
        prefix = '%s-' % self.request.user.pk
        files = os.listdir(settings.EXCEL_FILES_DIR)
        for file in files:
            if file.startswith(prefix):
                os.unlink(os.path.join(settings.EXCEL_FILES_DIR, file))

    def _save_tmp_file(self, file):
        name, ext = os.path.splitext(file.name)
        new_filename = '%s-%s%s' % (self.request.user.pk, int(time.time()), ext)
        default_storage.save(os.path.join(settings.EXCEL_FILES_DIR, new_filename), file)
        return new_filename

    def _delete_cached_data(self):
        self.request.session.pop('cached_excel_headers', None)
        self.request.session.pop('cached_excel_example_rows', None)

    def get_success_url(self):
        return reverse('webapp:import-mappings')


class ImportMappingsFormsetMixin(BaseTemplateView):
    permission = 'webapp.access_to_import'
    template_name = 'import/import_mappings.html'
    form_class = ImportMappingsForm
    base_formset_class = BaseImportMappingsFormSet

    EXAMPLE_ROWS_COUNT = 3

    exclude_site_model_fields = ['id', 'pws']
    formset = None
    excel_parser = None

    def get_site_model_fields_list(self):
        field_names = []
        for field in models.Site._meta.fields:
            if field.name not in self.exclude_site_model_fields:
                field_names.append(field.name)
        return field_names

    def get_site_model_fields_labels(self, fields_list):
        field_labels = []
        for field in models.Site._meta.fields:
            if field.name in fields_list:
                field_labels.append(field.verbose_name)
        return field_labels

    def get_site_model_fields_help_texts(self, fields_list):
        field_help_texts = []
        for field in models.Site._meta.fields:
            if field.name in fields_list:
                field_help_texts.append(field.help_text)
        return field_help_texts

    def get_site_model_required_fields(self, fields_list):
        required_fields = []
        for field in models.Site._meta.fields:
            if field.name in fields_list and (not field.null and field.default == NOT_PROVIDED):
                required_fields.append(field.name)
        return required_fields

    def get_excel_field_headers_as_choices(self):
        if 'cached_excel_headers' in self.request.session:
            return self.request.session['cached_excel_headers']
        headers = self.excel_parser.get_headers_as_choices()
        self.request.session['cached_excel_headers'] = headers
        return headers

    def get_excel_example_rows(self, rows_count=EXAMPLE_ROWS_COUNT):
        if 'cached_excel_example_rows' in self.request.session:
            return self.request.session['cached_excel_example_rows']
        example_rows = self.excel_parser.get_example_rows(rows_count)
        self.request.session['cached_excel_example_rows'] = example_rows
        return example_rows

    def get_formset(self):
        self.excel_parser = ExcelParser(os.path.join(settings.EXCEL_FILES_DIR, self.request.session['import_filename']))

        formset_class = formset_factory(form=self.form_class, formset=self.base_formset_class, extra=0)

        model_fields_list = self.get_site_model_fields_list()

        model_fields_for_form = [{'model_field': field_name} for field_name in model_fields_list]
        formset = formset_class(initial=model_fields_for_form, data=self.get_formset_data())

        model_fields_labels = self.get_site_model_fields_labels(model_fields_list)
        formset.set_model_fields_labels(model_fields_labels)

        model_fields_help_texts = self.get_site_model_fields_help_texts(model_fields_list)
        formset.set_model_fields_help_texts(model_fields_help_texts)

        model_required_fields = self.get_site_model_required_fields(model_fields_list)
        formset.set_required_model_fields(model_required_fields)

        excel_field_choices = self.get_excel_field_headers_as_choices()
        sorted_excel_field_choices = sorted(excel_field_choices, key=lambda item: item[1])
        formset.set_excel_field_choices(sorted_excel_field_choices)

        return formset

    def get_context_data(self, **kwargs):
        context = super(ImportMappingsFormsetMixin, self).get_context_data(**kwargs)
        context['formset'] = self.formset
        context['rows_count'] = (self.formset.total_form_count() - 1) / 2 + 1
        context['excel_example_rows'] = self.get_excel_example_rows()
        context['excel_field_headers'] = self.get_excel_field_headers_as_choices()
        if 'import_mappings' in self.request.session:
            context['import_mappings'] = json.dumps(self.request.session['import_mappings'])
        return context

    def get_formset_data(self):
        return None


class ImportMappingsRenderView(ImportMappingsFormsetMixin):
    def get(self, request, *args, **kwargs):
        self.formset = self.get_formset()
        return self.render_to_response(self.get_context_data())


class ImportMappingsProcessView(ImportMappingsFormsetMixin):
    def post(self, request, *args, **kwargs):
        self.formset = self.get_formset()
        if self.formset.is_valid():
            return self._import_excel_file()
        else:
            return self.render_to_response(self.get_context_data())

    def _import_excel_file(self):
        mappings = self.formset.get_mappings()
        self.request.session['import_mappings'] = mappings
        try:
            self._try_to_import(mappings)
            return redirect('webapp:import-mappings')
        except ExcelValidationError as e:
            for error in e.required_value_errors:
                self.formset.add_error(error)
            for error in e.date_format_errors:
                self.formset.add_error(error)
            for error in e.foreign_key_errors:
                self.formset.add_error(error)
            for error in e.numeric_errors:
                self.formset.add_error(error)
            return self.render_to_response(self.get_context_data())

    def _try_to_import(self, mappings):
        pws = models.PWS.active_only.get(pk=self.request.session.get('import_pws_pk'))
        date_format = self.request.session.get('import_date_format')
        self.excel_parser.check_constraints(mappings, date_format)
        import_log = models.ImportLog.objects.create(user=self.request.user, pws=pws)
        self.request.session['import_log_pk'] = import_log.pk
        update_only = self.request.session.get('import_update_only')
        self._run_background_parser(self.request.session['import_filename'], date_format,
                                    import_log, mappings, update_only)

    def _run_background_parser(self, filename, date_format, import_log, mappings, update_only):
        background_runner = BackgroundExcelParserRunner()
        background_runner.filename = filename
        background_runner.mappings = mappings
        background_runner.date_format = date_format
        background_runner.import_log_pk = import_log.pk
        background_runner.update_only = update_only
        background_runner.execute()

    def get_formset_data(self):
        return self.request.POST


class ImportProgressView(BaseTemplateView):
    permission = 'webapp.access_to_import'

    def get(self, request, *args, **kwargs):
        try:
            import_log_pk = self.request.session['import_log_pk']
            import_log = models.ImportLog.objects.get(pk=import_log_pk)
            progress = import_log.progress
            if progress == FINISHED:
                if import_log.duplicates_file:
                    messages.warning(self.request, Messages.Import.import_finished_duplicates % (
                        import_log.duplicates_count,
                        import_log.duplicates_file.url,
                        import_log.added_sites.count(),
                        import_log.updated_sites.count(),
                        import_log.deactivated_sites.count()
                    ))
                else:
                    messages.success(self.request, Messages.Import.import_was_finished % (
                        import_log.added_sites.count(),
                        import_log.updated_sites.count(),
                        import_log.deactivated_sites.count()
                    ))
                del self.request.session['import_log_pk']
                del self.request.session['import_pws_pk']
                del self.request.session['import_date_format']
        except ObjectDoesNotExist as e:
            del self.request.session['import_log_pk']
            del self.request.session['import_pws_pk']
            del self.request.session['import_date_format']
            print e.message
            progress = FINISHED
        except KeyError as e:
            print e.message
            progress = FINISHED
        return JsonResponse({'progress': progress})


class ImportLogListView(BaseTemplateView):
    permission = 'webapp.browse_import_log'
    template_name = 'import/import_log_list.html'

    def get_context_data(self, **kwargs):
        context = super(ImportLogListView, self).get_context_data(**kwargs)
        context['import_logs'] = self._get_import_logs()
        return context

    def _get_import_logs(self):
        queryset = models.ImportLog.objects.none()
        if self.request.user.has_perm('webapp.access_to_all_import_logs'):
            queryset = models.ImportLog.objects.all()
        elif self.request.user.has_perm('webapp.access_to_pws_import_logs'):
            queryset = models.ImportLog.objects.filter(pws__in=self.request.user.employee.pws.all())
        return queryset.order_by('-datetime')


class ImportLogSitesMixin(BaseTemplateView):
    permission = 'webapp.browse_import_log'
    template_name = 'home.html'

    def get_datetime_readable_value(self, import_log):
        return import_log.datetime.strftime('%b. %d, %Y, %H:%M')

    def get_context_data(self, **kwargs):
        context = super(ImportLogSitesMixin, self).get_context_data(**kwargs)
        import_log = models.ImportLog.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.ImportLogPermChecker.has_perm(self.request, import_log):
            raise Http404
        context['import_log'] = import_log
        header = self.get_header(import_log)
        if len(header.strip()) > 0:
            context['header'] = header
        sites = self.get_sites(import_log)
        context['site_filter'] = filters.SiteFilter(self.request.GET, queryset=sites, user=self.request.user)
        return context


class ImportLogAddedSitesView(ImportLogSitesMixin):
    def get_sites(self, import_log):
        return import_log.added_sites

    def get_header(self, import_log):
        return Messages.Import.added_sites_header % self.get_datetime_readable_value(import_log)


class ImportLogUpdatedSitesView(ImportLogSitesMixin):
    def get_sites(self, import_log):
        return import_log.updated_sites

    def get_header(self, import_log):
        return Messages.Import.updated_sites_header % self.get_datetime_readable_value(import_log)


class ImportLogDeactivatedSitesView(ImportLogSitesMixin):
    def get_sites(self, import_log):
        return import_log.deactivated_sites

    def get_header(self, import_log):
        return Messages.Import.deactivated_sites_header % self.get_datetime_readable_value(import_log)
