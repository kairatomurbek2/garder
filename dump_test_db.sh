#!/bin/bash

. virtualenv/bin/activate
python bigsurvey/manage.py dumpdata webapp auth --exclude=auth.permission --natural-foreign --settings=main.settings_test > bigsurvey/webapp_features/test.json
deactivate