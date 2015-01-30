#!/bin/sh

. virtualenv/bin/activate
bash dump_test_db.sh
python bigsurvey/manage.py harvest --settings=main.settings_test bigsurvey/webapp_features/features
deactivate