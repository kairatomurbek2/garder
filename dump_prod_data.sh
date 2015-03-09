#!/bin/sh
set -e
. ./virtualenv/bin/activate
cd ./bigsurvey/
FIXTURE_DIR=webapp/fixtures
./manage.py dumpdata webapp.sourcetype webapp.sitetype webapp.siteuse webapp.servicetype webapp.surveytype webapp.bptype webapp.bpsize webapp.bpmanufacturer webapp.customercode webapp.hazardtype webapp.testmanufacturer webapp.icpointtype webapp.assemblylocation webapp.assemblystatus webapp.lettertype webapp.floorscount webapp.special webapp.orientation webapp.sitestatus webapp.statictext --indent=2 > ${FIXTURE_DIR}/data_base.json
./manage.py dumpdata webapp.employee auth --exclude=auth.permission --natural-foreign --indent 2 > ${FIXTURE_DIR}/data_auth.json
for data_type in "customer" "pws" "site" "survey" "hazard" "letter"
do
   ./manage.py dumpdata webapp.${data_type} --indent=2 > ${FIXTURE_DIR}/dumpdata_${data_type}.json
done
deactivate
