from webapp_features.features.definitions.core.form_interactors import _browser_interactor


def filter_by_username(username_fragment):
    _browser_interactor.enter_into_field('username', username_fragment)
    _browser_interactor.submit_form()


def filter_by_user_group(user_group):
    _browser_interactor.select_option('user_group', user_group)
    _browser_interactor.submit_form()


def filter_by_record_object(record_object_text_fragment):
    _browser_interactor.enter_into_field('record_object', record_object_text_fragment)
    _browser_interactor.submit_form()
