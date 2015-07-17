#!/bin/sh
set -e
. ./virtualenv/bin/activate
cd ./bigsurvey/
FIXTURE_DIR=webapp/fixtures
./manage.py dumpdata webapp.sourcetype webapp.sitetype webapp.siteuse webapp.servicetype webapp.surveytype webapp.bpsize webapp.bpmanufacturer webapp.customercode webapp.hazardtype webapp.testmanufacturer webapp.testmodel webapp.icpointtype webapp.assemblylocation webapp.assemblystatus webapp.lettertype webapp.floorscount webapp.special webapp.orientation webapp.sitestatus --indent=2 > ${FIXTURE_DIR}/data_base.json
./manage.py dumpdata auth.group --natural-foreign --indent 2 > ${FIXTURE_DIR}/data_perms.json
./manage.py dumpdata webapp.employee auth.user --natural-foreign --indent 2 > ${FIXTURE_DIR}/data_users.json
for data_type in "pws" "survey" "hazard" "letter"
do
   ./manage.py dumpdata webapp.${data_type} --indent=2 > ${FIXTURE_DIR}/data_${data_type}.json
done
./manage.py dump_object webapp.site `seq 1 6000` > ${FIXTURE_DIR}/data_site_1.json
./manage.py dump_object webapp.site `seq 6001 12000` > ${FIXTURE_DIR}/data_site_2.json
./manage.py dump_object webapp.site `seq 12001 18000` > ${FIXTURE_DIR}/data_site_3.json
./manage.py dump_object webapp.site `seq 18001 24000` > ${FIXTURE_DIR}/data_site_4.json
./manage.py dump_object webapp.site `seq 24001 30000` > ${FIXTURE_DIR}/data_site_5.json
./manage.py dump_object webapp.site `seq 30001 35278` > ${FIXTURE_DIR}/data_site_6.json
./manage.py dumpdata webapp.statictext --indent=2 > ${FIXTURE_DIR}/data_help.json
deactivate
