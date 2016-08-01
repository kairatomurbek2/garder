#!/bin/sh
set -e
echo =================== RESTORE BACKUP PWS ===================
python_path=${1}
FILE_PATH="/tmp/backup/$2/$3/"
pwd FILE_PATH
for data_type in "pws" "users" "employees" "sites" "hazards" "bp_devices" "surveys" "letter_type" "test_kit" "test_cert" "tests" "import_log"
do
    for part_number in `seq 0 100`
    do
        FILE_NAME="${FILE_PATH}${data_type}_${part_number}.json"
        if [ -f ${FILE_NAME} ]; then
            echo Loading ${FILE_NAME}
            ${python_path} manage.py loaddata ${FILE_NAME}
        fi
    done
done


