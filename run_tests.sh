#!/bin/sh

. virtualenv/bin/activate
python bigsurvey/manage.py harvest
deactivate