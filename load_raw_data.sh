#!/bin/sh
set -e
. ./virtualenv/bin/activate
cd ./bigsurvey/
FILE_PATH="./webapp/fixtures/raw/"
FILE_PREFIX="raw_data_"
for data_type in "base" "pws" "perms" "users" "testers" "site" "hazard" "survey" "test_kit" "tester_cert" "test" "letter" "regulation"
do
    for part_number in `seq 0 100`
    do
        FILE_NAME="${FILE_PATH}${FILE_PREFIX}${data_type}_${part_number}.json"
        if [ -f ${FILE_NAME} ]; then
            echo Loading ${FILE_NAME}
            ./manage.py loaddata ${FILE_NAME}
        fi
    done
done
deactivate
