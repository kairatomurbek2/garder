#!/bin/bash

if [ ! -d "virtualenv" ]; then
    virtualenv --no-site-packages --distribute virtualenv
fi
. virtualenv/bin/activate
pip install -r requirements.txt
cd bigsurvey
./manage.py migrate --noinput
./manage.py loaddata test
deactivate
