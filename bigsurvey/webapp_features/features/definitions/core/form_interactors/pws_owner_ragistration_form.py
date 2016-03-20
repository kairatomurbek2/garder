# -*- coding: utf-8 -*-
from webapp_features.features.definitions.core import finder
from webapp_features.features.definitions.core.form_interactors._browser_interactor import (
    submit_form
)


def fill_in_multiple_textfields(step):
    for row in step.hashes:
        step.given('I fill in "%s" with "%s"' % (row['field'], row['value']))


def checkbox_click():
    finder.find_element_by_id('form-s-c').click()


def submit():
    submit_form()
