#!/bin/sh
set -e
. ./virtualenv/bin/activate
cd ./bigsurvey/
for data_type in "base" "pws_0" "perms" "users" "site_0" "site_1" "site_2" "site_3" "site_4" "site_5" "site_6" "site_7" "site_8" "site_9" "site_10" "site_11" "site_12" "site_13" "site_14" "site_15" "site_16" "site_17" "site_18" "site_19" "site_20" "site_21" "hazard_0" "hazard_1" "hazard_2" "hazard_3" "survey_0" "survey_1" "survey_2" "survey_3" "letter_0"
do
   echo Loading ${data_type}
   ./manage.py loaddata raw_data_${data_type}
done
deactivate
