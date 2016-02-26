from webapp_features.features.definitions.core.navigators import _common


def go_to_registration_page():
    _common.go_to_url('/registration/')


def go_to_activate_page():
    _common.go_to_url('/activate-blocked-pws/')
