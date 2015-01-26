#!/bin/sh

. virtualenv/bin/activate
python bigsurvey/manage.py harvest --settings="main.settings_test" bigsurvey/webapp_features/features
deactivate