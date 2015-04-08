#!/bin/sh
set -e
. ./virtualenv/bin/activate
cd ./bigsurvey/
for data_type in "base" "pws" "auth" "help" "cust_1" "cust_2" "cust_3" "site_1" "site_2" "site_3" "hazard" "survey" "letter"
do
   echo Loading ${data_type}s
   ./manage.py loaddata data_${data_type}
done
deactivate
