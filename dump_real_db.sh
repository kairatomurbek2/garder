#!/bin/bash

. virtualenv/bin/activate
python bigsurvey/manage.py dumpdata webapp auth --exclude=auth.permission --natural-foreign > bigsurvey/webapp/fixtures/data.json
deactivate