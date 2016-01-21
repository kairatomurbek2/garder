# -*- coding: utf-8 -*-
"""
In this file we define common functions that may be useful
in all feature steps.
"""
from lettuce.django import mail
from webapp_features.features.definitions.core.form_interactors import (
    login_form
)
from webapp_features.features.definitions.core.navigators import (
    home_navigator
)


def login(username, password):
    home_navigator.go_to_login_page()
    login_form.enter_username(username)
    login_form.enter_password(password)
    login_form.submit()


def root_admin_logs_in():
    home_navigator.go_to_login_page()
    login('root', '1qaz@WSX')


def super_admin_logs_in():
    home_navigator.go_to_login_page()
    login('superadmin', 'superadmin')


def owner_logs_in():
    home_navigator.go_to_login_page()
    login('owner', 'admin')


def admin_logs_in():
    home_navigator.go_to_login_page()
    login('admin', 'admin')


def surveyor_logs_in():
    home_navigator.go_to_login_page()
    login('surveyor', 'surveyor')


def tester_logs_in():
    home_navigator.go_to_login_page()
    login('tester', 'tester')


def read_email():
    email_obj = mail.queue.get(block=True, timeout=15)
    return email_obj
