#!/bin/bash

if [ ! -d "virtualenv" ]; then
    virtualenv --no-site-packages --distribute virtualenv
fi
. virtualenv/bin/activate
pip install -r requirements.txt
cd bigsurvey
./manage.py migrate
for data_type in "base" "pws" "auth" "help" "details" "site_1" "site_2" "site_3" "site_4" "site_5" "site_6" "hazard" "survey" "letter"
do
   echo Loading ${data_type}s
   ./manage.py loaddata data_${data_type}
done
./manage.py collectstatic --noinput
touch main/wsgi.py
deactivate
