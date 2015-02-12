#!/bin/bash

. virtualenv/bin/activate
cd bigsurvey
./manage.py harvest --settings=main.settings_test webapp_features/features
deactivate