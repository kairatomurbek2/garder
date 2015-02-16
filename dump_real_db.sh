#!/bin/sh

. virtualenv/bin/activate
cd bigsurvey
./manage.py dumpdata webapp auth --exclude=auth.permission --natural-foreign --indent=2 > ./webapp_features/fixtures/data.json
deactivate