#!/bin/bash

source ./virtualenv/bin/activate
cd bigsurvey
python manage.py $@
cd ../
