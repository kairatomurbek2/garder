# -*- coding: utf-8 -*-
from webapp_features.features.definitions.core.form_interactors._browser_interactor import (
    enter_into_field, submit_form
)

def enter_email(email):
    enter_into_field(field_name='email', text=email)

def enter_new_password(password):
    enter_into_field(field_name='new_password1', text=password)
    enter_into_field(field_name='new_password2', text=password)

def submit():
    submit_form()
