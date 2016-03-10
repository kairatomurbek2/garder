from smtplib import SMTPException
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from main import settings
from main.parameters import Messages, Groups, OWNER_GROUPS, ADMIN_GROUPS
from webapp import models, forms, perm_checkers
from webapp.actions.builders import UserManagementActionsBuilder
from webapp.actions.users import UserAdditionException
from .base_views import BaseTemplateView, BaseFormView


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

    @staticmethod
    def administrator_group_name():
        return Groups.admin


class UserBaseFormView(BaseFormView):
    user_model = models.User
    user_object = None
    employee_model = models.Employee
    employee_form_class = forms.EmployeeForm
    cert_form_class = forms.TesterCertForm
    test_kit_form_class = forms.TestKitForm
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
        if self.request.user.has_perm('webapp.access_to_pws_test_kits')\
                and self.request.user.has_perm('webapp.access_to_pws_tester_certs'):
            context['test_kit_form'] = self.get_test_kit_form()
            context['cert_form'] = self.get_cert_form()
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
        queryset = models.PWS.active_only.none()
        if self.request.user.has_perm('webapp.access_to_pws_users'):
            if self.request.user.employee.pws.all():
                queryset = self.request.user.employee.pws.all()
        if self.request.user.has_perm('webapp.access_to_all_users'):
            queryset = models.PWS.active_only.all()
        return queryset

    def get_success_url(self):
        return reverse('webapp:user_list')

    def get_test_kit_form(self):
        return self.test_kit_form_class(**self.get_form_kwargs())

    def get_cert_form(self):
        return self.cert_form_class(**self.get_form_kwargs())


class UserAddView(UserBaseFormView):
    permission = 'auth.add_user'
    user_form_class = forms.UserAddForm
    success_message = Messages.User.adding_success

    def post(self, request, *args, **kwargs):
        action = UserManagementActionsBuilder.get_user_add_action(request.user,
                                                                  self.get_user_form(),
                                                                  self.get_employee_form(),
                                                                  self.get_test_kit_form(),
                                                                  self.get_cert_form())

        try:
            action.execute()
            messages.success(self.request, self.success_message)
            return redirect(self.get_success_url())
        except UserAdditionException as e:
            messages.error(self.request, e.message)
            action.user_form.fields['groups'].queryset = self._get_queryset_for_group_field()
            action.employee_form.fields['pws'].queryset = self._get_queryset_for_pws_field()
            return render(self.request, self.template_name,
                          {'user_form': action.user_form,
                           'employee_form': action.employee_form,
                           'test_kit_form': action.test_kit_form,
                           'cert_form': action.cert_form})

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
            if Group.objects.get(name=Groups.tester) in selected_user.groups.all() and selected_user.has_perm('webapp.can_own_test_kit'):
                context['is_tester'] = True
            return context
        raise Http404


class UserEditView(UserBaseFormView):
    permission = 'auth.change_user'
    user_form_class = forms.UserEditForm
    success_message = Messages.User.editing_success
    error_message = Messages.User.editing_error

    def get_form_kwargs(self):
        kwargs = super(UserEditView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
        if self._changing_self_group_is_not_allowed(user):
            context['do_not_show_groups'] = True
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
                if self.request.user.is_superuser or self.request.user.groups.filter(name=Groups.superadmin):
                    pws_to_save = employee_form.cleaned_data['pws']
                else:
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
            return render(self.request, self.template_name,
                          {
                              'user_form': user_form,
                              'employee_form': employee_form,
                              'display_is_active': True
                          })

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

    def _changing_self_group_is_not_allowed(self, user):
        user_obj_and_request_user_is_admin = self._user_in_admin_group(user)
        user_obj_and_request_user_is_owner = self._user_in_pws_owner_group(user)
        return user_obj_and_request_user_is_admin or user_obj_and_request_user_is_owner

    def _user_in_admin_group(self, user):
        request_user_is_admin = Groups.admin in [group.name for group in self.request.user.groups.all()]
        user_obj_is_admin = Groups.admin in [group.name for group in user.groups.all()]
        return request_user_is_admin and user_obj_is_admin

    def _user_in_pws_owner_group(self, user):
        request_user_is_pws_owner = Groups.pws_owner in [group.name for group in self.request.user.groups.all()]
        user_obj_is_pws_owner = Groups.pws_owner in [group.name for group in user.groups.all()]
        return request_user_is_pws_owner and user_obj_is_pws_owner


class UserSearchView(BaseFormView):
    template_name = 'user/user_search.html'
    form_class = forms.UserSearchForm
    permission = 'webapp.browse_user'
    users = models.User.objects.none()

    def post(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())
        if form.is_valid():
            self.users = self.__get_users(form)
            if 'invite_user' in request.POST:
                invite_form = forms.UserInviteForm(
                    pws_queryset=self.request.user.employee.pws.all(),
                    users=self.users,
                    **self.get_form_kwargs()
                )
                if invite_form.is_valid():
                    return self.invite_form_valid(invite_form)
                return self.invite_form_invalid(form, invite_form)
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        invite_form = None
        if self.users:
            invite_form = forms.UserInviteForm(
                pws_queryset=self.request.user.employee.pws.all(),
                users=self.users
            )
        else:
            messages.error(self.request, Messages.UserInvite.user_not_found)
        return self.render_to_response({'form': form, 'users': self.users, 'invite_form': invite_form})

    def __get_users(self, form):
        group = form.cleaned_data['group']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        cert_number = form.cleaned_data['cert_number']
        users = User.objects.filter(groups=group)
        if username:
            users = users.filter(username=username)
        if email:
            users = users.filter(email=email)
        if group.name == Groups.tester and cert_number:
            users = users.filter(certs__cert_number=cert_number)
        return users

    def invite_form_valid(self, invite_form):
        invite = self.__create_invite(invite_form)
        self.__send_email_to_user(invite, invite_form.cleaned_data['user'])
        return HttpResponseRedirect(reverse('webapp:user_list'))

    def __create_invite(self, invite_form):
        user = invite_form.cleaned_data['user']
        selected_pws = invite_form.cleaned_data['pws']
        invite = models.Invite.objects.create(
            invite_from=self.request.user,
            invite_to=user,
        )
        for pws in selected_pws:
            if pws not in user.employee.pws.all():
                invite.invite_pws.add(pws)
        invite.save()
        return invite

    def __send_email_to_user(self, invite, user):
        context = {
            'invite': invite,
            'base_url': settings.HOST
        }
        html_template = 'email_templates/html/pws_invite_notification.html'
        plain_template = 'email_templates/plain/pws_invite_notification.txt'
        subject = 'Invitation from PWS'
        html_content = render_to_string(html_template, context)
        plain_content = render_to_string(plain_template, context)
        try:
            user.email_user(
                subject=subject,
                message=plain_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_message=html_content
            )
            messages.success(self.request, Messages.UserInvite.user_invite_success)
        except SMTPException:
            messages.error(self.request, Messages.UserInvite.user_invite_failed)

    def invite_form_invalid(self, form, invite_form):
        messages.error(self.request, Messages.UserInvite.user_invite_error)
        return self.render_to_response({'form': form, 'users': self.users, 'invite_form': invite_form})


class UserInviteAcceptView(BaseTemplateView):
    template_name = 'user/user_invite_accept.html'

    def get(self, request, *args, **kwargs):
        try:
            invite = models.Invite.objects.get(code=request.GET.get('code'))
        except ObjectDoesNotExist:
            raise Http404
        if invite.invite_to != request.user:
            raise Http404
        if invite.accepted:
            invite_message = "You have already accepted this invite."
        elif (datetime.now().date() - invite.invite_date).days > 3:
            invite_message = "Invite expired. Please, contact PWS administrator to receive new invite."
        else:
            for pws in invite.invite_pws.all():
                invite.invite_to.employee.pws.add(pws)
            invite.invite_to.employee.save()
            invite.accepted = True
            invite.save()
            invite_message = "Invite successfully accepted."
        self.__send_email_to_admin(invite)
        context = self.get_context_data(**kwargs)
        context['invite_accept_text'] = invite_message
        return self.render_to_response(context)

    def __send_email_to_admin(self, invite):
        context = {
            'invite': invite,
        }
        html_template = 'email_templates/html/pws_invite_accept_notification.html'
        plain_template = 'email_templates/plain/pws_invite_accept_notification.txt'
        subject = 'Invitation have been accepted'
        html_content = render_to_string(html_template, context)
        plain_content = render_to_string(plain_template, context)
        try:
            invite.invite_from.email_user(
                subject=subject,
                message=plain_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_message=html_content
            )
        except SMTPException:
            pass
