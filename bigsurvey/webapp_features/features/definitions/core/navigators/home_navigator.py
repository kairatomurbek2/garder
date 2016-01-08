# -*- coding: utf-8 -*-
from webapp_features.features.definitions.core.navigators import _common


def go_to_login_page():
    _common.go_to_url('/accounts/logout')
