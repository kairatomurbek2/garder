#!/bin/bash

. virtualenv/bin/activate
cd bigsurvey
RUN_TEST_COMMAND="./manage.py harvest webapp_features/features --settings=main.settings_test --with-xunit --xunit-file=../testres.xml"
for var in ${@}
do
    RUN_TEST_COMMAND=${RUN_TEST_COMMAND}" -t ${var}"
done
bash -c "${RUN_TEST_COMMAND}"
deactivate