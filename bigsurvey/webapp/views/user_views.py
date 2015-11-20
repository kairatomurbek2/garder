from .base_views import BaseTemplateView, BaseFormView
from django.http import Http404
from django.core.urlresolvers import reverse
from webapp import models, forms, perm_checkers
from main.parameters import Messages, Groups, OWNER_GROUPS, ADMIN_GROUPS
from django.contrib import messages
from django.contrib.auth.models import User, Group
from collections import OrderedDict
from django.shortcuts import render, redirect


class UserListView(BaseTemplateView):
    permission = 'webapp.browse_user'
    template_name = 'user/user_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['user_lists'], context['user_groups'] = self._get_users()
        return context

    def _get_users(self):
        user_lists = []
        if self.request.user.has_perm('webapp.access_to_all_users'):
            user_groups = [
                'Super Administrators', 'PWS Owners', 'Administrators',
                'Surveyors', 'Testers', 'Administrative Authority', 'Without Group'
            ]
            user_lists.append(models.User.objects.filter(groups__name=Groups.superadmin))
            user_lists.append(models.User.objects.filter(groups__name=Groups.pws_owner))
            user_lists.append(models.User.objects.filter(groups__name=Groups.admin))
            user_lists.append(models.User.objects.filter(groups__name=Groups.surveyor))
            user_lists.append(models.User.objects.filter(groups__name=Groups.tester))
            user_lists.append(models.User.objects.filter(groups__name=Groups.ad_auth))
            user_lists.append(models.User.objects.filter(groups=None))
        elif self.request.user.has_perm('webapp.access_to_pws_users'):
            user_groups = ['Administrators', 'Surveyors', 'Testers', 'Without Group']
            if self.request.user.has_perm('webapp.access_to_multiple_pws_users'):
                user_groups.insert(0, 'PWS Owners')
                user_lists.append(models.User.objects.filter(
                    groups__name=Groups.pws_owner,
                    employee__pws__in=self.request.user.employee.pws.all()
                ).distinct())
            user_lists.append(models.User.objects.filter(
                groups__name=Groups.admin,
                employee__pws__in=self.request.user.employee.pws.all()
            ).distinct())
            user_lists.append(models.User.objects.filter(
                groups__name=Groups.surveyor,
                employee__pws__in=self.request.user.employee.pws.all()
            ))
            user_lists.append(models.User.objects.filter(
                groups__name=Groups.tester,
                employee__pws__in=self.request.user.employee.pws.all()
            ).distinct())
            user_lists.append(models.User.objects.filter(
                groups=None,
                employee__pws__in=self.request.user.employee.pws.all()
            ))
        else:
            raise Http404
        return user_lists, user_groups


class UserBaseFormView(BaseFormView):
    user_model = models.User
    user_object = None
    employee_model = models.Employee
    employee_form_class = forms.EmployeeForm
    employee_object = None
    template_name = 'user/user_form.html'

    def get(self, request, *args, **kwargs):
        user_form = self.get_user_form()
        employee_form = self.get_employee_form()
        user_form.fields['groups'].queryset = self._get_queryset_for_group_field()
        employee_form.fields['pws'].queryset = self._get_queryset_for_pws_field()
        context = self.get_context_data(**kwargs)
        context['user_form'] = user_form
        context['employee_form'] = employee_form
        return render(self.request, self.template_name, context)

    def _get_queryset_for_group_field(self):
        if self.request.user.has_perm('webapp.access_to_all_users'):
            queryset = Group.objects.all()
        elif self.request.user.has_perm('webapp.access_to_multiple_pws_users'):
            queryset = Group.objects.filter(name__in=OWNER_GROUPS)
        elif self.request.user.has_perm('webapp.access_to_pws_users'):
            queryset = Group.objects.filter(name__in=ADMIN_GROUPS)
        else:
            raise Http404
        return queryset

    def _get_queryset_for_pws_field(self):
        queryset = models.PWS.objects.none()
        if self.request.user.has_perm('webapp.access_to_pws_users'):
            if self.request.user.employee.pws.all():
                queryset = self.request.user.employee.pws.all()
        if self.request.user.has_perm('webapp.access_to_all_users'):
            queryset = models.PWS.objects.all()
        return queryset

    def get_success_url(self):
        return reverse('webapp:user_list')


class UserAddView(UserBaseFormView):
    permission = 'auth.add_user'
    user_form_class = forms.UserAddForm
    success_message = Messages.User.adding_success
    error_message = Messages.User.adding_error

    def post(self, request, *args, **kwargs):
        user_form = self.get_user_form()
        employee_form = self.get_employee_form()
        if user_form.is_valid() and employee_form.is_valid():
            self.user_object = user_form.save()
            employee_form.instance.user = self.user_object
            self.employee_object = employee_form.save()
            if not (self.request.user.has_perm('webapp.access_to_all_users') or self.request.user.has_perm('webapp.access_to_multiple_pws_users')):
                self.employee_object.pws = [self.request.user.employee.pws.all()[0]]
            self.employee_object.save()
            messages.success(self.request, self.success_message)
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, self.error_message)
            user_form.fields['groups'].queryset = self._get_queryset_for_group_field()
            employee_form.fields['pws'].queryset = self._get_queryset_for_pws_field()
            return render(self.request, self.template_name, {'user_form': user_form, 'employee_form': employee_form})

    def get_user_form(self):
        return self.user_form_class(**self.get_form_kwargs())

    def get_employee_form(self):
        if self.request.user.has_perm('webapp.access_to_all_users'):
            return forms.EmployeeFormNoPWS(instance=self.employee_object, **self.get_form_kwargs())
        form_kwargs = self.get_form_kwargs()
        form_kwargs['initial']['pws'] = [self.request.user.employee.pws.all().first()]
        return self.employee_form_class(instance=self.employee_object, **form_kwargs)


class UserDetailView(BaseTemplateView):
    template_name = "user/user_detail.html"
    permission = "webapp.browse_user"

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        selected_user = User.objects.get(pk=kwargs['pk'])
        if perm_checkers.UserPermChecker.has_perm(self.request, selected_user):
            context['selected_user'] = selected_user
            if Group.objects.get(name=Groups.tester) in selected_user.groups.all():
                context['is_tester'] = True
            return context
        raise Http404


class UserEditView(UserBaseFormView):
    permission = 'auth.change_user'
    user_form_class = forms.UserEditForm
    success_message = Messages.User.editing_success
    error_message = Messages.User.editing_error

    def get(self, request, *args, **kwargs):
        response = super(UserEditView, self).get(request, *args, **kwargs)
        if not perm_checkers.UserPermChecker.has_perm(self.request, self.user_object):
            raise Http404
        return response

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        user = self.user_model.objects.get(pk=self.kwargs['pk'])
        testers_group = models.Group.objects.get(name=Groups.tester)
        if testers_group not in user.groups.all() or self.request.user.has_perm('webapp.access_to_all_users'):
            context['display_is_active'] = True
        return context

    def post(self, request, *args, **kwargs):
        user = self.user_model.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.UserPermChecker.has_perm(self.request, user):
            raise Http404
        user_form = self.get_user_form()
        employee_form = self.get_employee_form()
        if user_form.is_valid() and employee_form.is_valid():
            if user_form.instance.pk == self.request.user.pk:
                self.user_object = user_form.save(commit=False)
                self.employee_object = employee_form.save(commit=False)
                self.user_object.groups = self.request.user.groups.all()
                self.employee_object.pws = self.request.user.employee.pws.all()
                self.user_object.is_active = True
                self.user_object.save()
                self.employee_object.save()
            else:
                self.user_object = user_form.save(commit=False)
                pws_to_save = user.employee.pws.all().exclude(id__in=self.request.user.employee.pws.all()) | employee_form.cleaned_data['pws']
                employee_form.cleaned_data['pws'] = pws_to_save
                self.employee_object = employee_form.save()
                testers_group = models.Group.objects.get(name=Groups.tester)
                if testers_group in self.user_object.groups.all() and not self.request.user.has_perm('webapp.access_to_all_users'):
                    self.user_object.is_active = True
                self.user_object.save()
            messages.success(self.request, self.success_message)
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, self.error_message)
            user_form.fields['groups'].queryset = self._get_queryset_for_group_field()
            employee_form.fields['pws'].queryset = self._get_queryset_for_pws_field()
            return render(self.request, self.template_name, {'user_form': user_form, 'employee_form': employee_form})

    def get_user_form(self):
        self.user_object = self.user_model.objects.get(pk=self.kwargs['pk'])
        if not perm_checkers.UserPermChecker.has_perm(self.request, self.user_object):
            raise Http404
        return self.user_form_class(instance=self.user_object, **self.get_form_kwargs())

    def get_employee_form(self):
        tester_group = models.Group.objects.get(name=Groups.tester)
        self.employee_object = self.employee_model.objects.get(user=self.user_object)
        if self.request.user.has_perm('webapp.access_to_all_users') or tester_group in self.user_object.groups.all():
            return forms.EmployeeFormNoPWS(instance=self.employee_object, **self.get_form_kwargs())
        return self.employee_form_class(instance=self.employee_object, **self.get_form_kwargs())
