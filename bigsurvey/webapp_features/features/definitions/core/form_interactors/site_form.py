from webapp_features.features.definitions.core.form_interactors import _browser_interactor


def select_yes_in_fire_present():
    _browser_interactor.select_option('fire_present', 'Yes')


def submit_form():
    _browser_interactor.submit_form()
