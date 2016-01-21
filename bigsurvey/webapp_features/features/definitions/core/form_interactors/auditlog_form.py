from webapp_features.features.definitions.core.form_interactors import _browser_interactor


def filter_by_username(username_fragment):
    _browser_interactor.enter_into_field('username', username_fragment)
    _browser_interactor.submit_form()
