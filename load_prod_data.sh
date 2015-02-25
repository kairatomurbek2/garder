#!/bin/sh
set -e
. ./virtualenv/bin/activate
cd ./bigsurvey/
for data_type in "base" "pws" "auth" "customer" "site" "survey" "hazard" "letter"
do
   echo Loading ${data_type}s
   ./manage.py loaddata data_${data_type}
done
deactivate
