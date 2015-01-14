#!bin/bash

virtualenv --no-site-packages --distribute virtualenv
. virtualenv/bin/activate
pip install -r requirements.txt
cd bigsurvey
./manage.py migrate
./manage.py loaddata data
deactivate
