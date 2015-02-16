#!/bin/sh

. virtualenv/bin/activate
cd bigsurvey
./manage.py dumpdata webapp auth --exclude=auth.permission --natural-foreign --indent=2 --settings=main.settings_test > ./webapp_features/fixtures/test.json
deactivate