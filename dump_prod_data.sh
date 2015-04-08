#!/bin/sh
set -e
. ./virtualenv/bin/activate
cd ./bigsurvey/
FIXTURE_DIR=webapp/fixtures
./manage.py dumpdata webapp.sourcetype webapp.sitetype webapp.siteuse webapp.servicetype webapp.surveytype webapp.bptype webapp.bpsize webapp.bpmanufacturer webapp.customercode webapp.hazardtype webapp.testmanufacturer webapp.testmodel webapp.icpointtype webapp.assemblylocation webapp.assemblystatus webapp.lettertype webapp.floorscount webapp.special webapp.orientation webapp.sitestatus --indent=2 > ${FIXTURE_DIR}/data_base.json
./manage.py dumpdata webapp.employee auth --exclude=auth.permission --natural-foreign --indent 2 > ${FIXTURE_DIR}/data_auth.json
for data_type in "customer" "pws" "survey" "hazard" "letter"
do
   ./manage.py dumpdata webapp.${data_type} --indent=2 > ${FIXTURE_DIR}/data_${data_type}.json
done
./manage.py dump_object webapp.site `seq 1 12000` > ${FIXTURE_DIR}/data_site_1.json
./manage.py dump_object webapp.site `seq 12001 24000` > ${FIXTURE_DIR}/data_site_2.json
./manage.py dump_object webapp.site `seq 24000 35278` > ${FIXTURE_DIR}/data_site_3.json
./manage.py dumpdata webapp.statictext --indent=2 > ${FIXTURE_DIR}/data_help.json
deactivate
