#!/bin/bash

. virtualenv/bin/activate
cd bigsurvey
# unit tests
./manage.py test webapp_features --settings=main.settings_test


# acceptance tests
RUN_TEST_COMMAND="./manage.py harvest webapp_features/features --settings=main.settings_test --debug-mode --with-xunit --xunit-file=../testres.xml"
for var in ${@}
do
    RUN_TEST_COMMAND=${RUN_TEST_COMMAND}" -t ${var}"
done
bash -c "${RUN_TEST_COMMAND}"
deactivate