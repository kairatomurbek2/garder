#!/bin/bash

if [ ! -d "virtualenv" ]; then
    virtualenv --no-site-packages --distribute virtualenv
fi
. virtualenv/bin/activate
pip install -r requirements.txt
cd bigsurvey
./manage.py migrate --noinput
FILE_PATH="./webapp/fixtures/raw/"
FILE_PREFIX="raw_data_"
for data_type in "base" "pws" "perms" "users" "testers" "site" "hazard" "survey" "test_kit" "tester_cert" "test" "letter" "regulation"
do
    for part_number in 0 `seq 50`
    do
        FILE_NAME="${FILE_PATH}${FILE_PREFIX}${data_type}_${part_number}.json"
        if [ -f ${FILE_NAME} ]; then
            echo Loading fixture ${FILE_NAME}...
            ./manage.py loaddata ${FILE_NAME}
        fi
    done
done
echo Creating lettertypes...
./manage.py create_lettertypes_for_pws
echo Settings dates...
./manage.py set_last_survey_date
./manage.py set_due_install_test_date
echo Creating initial revisions...
./manage.py createinitialrevisions
echo Collecting static...
./manage.py collectstatic --noinput
touch main/wsgi.py
deactivate
