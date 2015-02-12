#!/bin/bash

if [ ! -d "virtualenv" ]; then
    virtualenv --no-site-packages --distribute virtualenv
fi
. virtualenv/bin/activate
pip install -r requirements.txt
cd bigsurvey
./manage.py migrate
./manage.py loaddata base_data
./manage.py collectstatic --noinput
touch main/wsgi.py
deactivate
