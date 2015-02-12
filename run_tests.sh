#!/bin/bash

. virtualenv/bin/activate
cd bigsurvey
./manage.py harvest webapp_features/features --settings=main.settings_test --with-xunit --xunit-file=../testres.xml
deactivate