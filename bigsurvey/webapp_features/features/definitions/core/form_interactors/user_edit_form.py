from webapp_features.features.definitions.core.form_interactors import _browser_interactor


def change_username(new_username):
    _browser_interactor.enter_into_field('username', new_username)
    _browser_interactor.submit_form()
