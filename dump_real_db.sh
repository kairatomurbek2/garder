#!/bin/sh

. virtualenv/bin/activate
python bigsurvey/manage.py dumpdata webapp auth --exclude=auth.permission --natural-foreign > bigsurvey/webapp_features/fixtures/data.json
deactivate