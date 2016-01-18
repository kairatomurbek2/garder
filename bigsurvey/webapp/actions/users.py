from main.parameters import Messages


class UserAdditionException(Exception):
    pass


class UserAddtionUserFormNotProvidedException(UserAdditionException):
    pass


class AddUserAction(object):
    user = None
    user_form = None
    employee_form = None
    test_kit_form = None
    cert_form = None

    def execute(self):
        if not self.user_form:
            raise UserAddtionUserFormNotProvidedException()
        if self.user_form.is_valid() and self.employee_form.is_valid():
            user_object = self.user_form.save()
            self.employee_form.instance.user = user_object
            employee_object = self.employee_form.save()
            if not (self.user.has_perm('webapp.access_to_all_users') or self.user.has_perm(
                    'webapp.access_to_multiple_pws_users')):
                employee_object.pws = [self.user.employee.pws.all()[0]]
            employee_object.save()
            if self._user_object_is_in_testers_group(user_object) and self._user_has_permissions():
                if self.test_kit_form.is_valid() and self.cert_form.is_valid():
                    self.test_kit_form.instance.user = user_object
                    self.test_kit_form.save()
                    self.cert_form.instance.user = user_object
                    self.cert_form.save()
                else:
                    raise UserAdditionException(Messages.User.adding_error)
        else:
            raise UserAdditionException(Messages.User.adding_error)

    @staticmethod
    def _user_object_is_in_testers_group(user_object):
        return u'Testers' in [group.name for group in user_object.groups.all()]

    def _user_has_permissions(self):
        return self.user.has_perm('webapp.access_to_pws_test_kits') \
               and self.user.has_perm('webapp.access_to_pws_tester_certs')
