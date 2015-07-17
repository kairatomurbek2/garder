#!/bin/sh
set -e
. ./virtualenv/bin/activate
cd ./bigsurvey/
for data_type in "base" "pws" "perms" "users" "help" "site_1" "site_2" "site_3" "site_4" "site_5" "site_6" "hazard" "survey" "letter"
do
   echo Loading ${data_type}
   ./manage.py loaddata data_${data_type}
done
deactivate
