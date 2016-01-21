# -*- coding: utf-8 -*-
from webapp_features.features.definitions.core.navigators import _common


def go_to_login_page():
    _common.go_to_url('/accounts/logout')


def go_to_users_page():
    _common.go_to_url('/user/')


def go_to_auditlog_page():
    _common.go_to_url('/audit-log')
