from webapp.actions.users import AddUserAction


class UserManagementActionsBuilder(object):
    @staticmethod
    def get_user_add_action(user, user_form, employee_form, test_kit_form, cert_form):
        action = AddUserAction()
        action.user = user
        action.user_form = user_form
        action.employee_form = employee_form
        action.test_kit_form = test_kit_form
        action.cert_form = cert_form
        return action
