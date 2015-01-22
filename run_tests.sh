#!/bin/sh

. virtualenv/bin/activate
python bigsurvey/manage.py harvest --settings="main.settings_test" bigsurvey/webapp/features
deactivate