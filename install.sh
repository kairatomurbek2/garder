#!/bin/bash

if [ ! -d "virtualenv" ]; then
    virtualenv --no-site-packages --distribute virtualenv
fi
. virtualenv/bin/activate
echo ===================== INSTALLING REQUIREMENTS ======================
pip install -r requirements.txt
cd ./bigsurvey
echo =================== MIGRATING DATABASE STRUCTURE ===================
./manage.py migrate --noinput
echo =========================== LOADING DATA ===========================
#cd ../
#bash ./load_raw_data.sh
#cd ./bigsurvey
echo ====================== CREATING LETTER TYPES =======================
./manage.py create_lettertypes_for_pws
echo ========================== SETTING DATES ===========================
./manage.py set_last_survey_date
./manage.py set_due_install_test_date
echo ==================== CREATING INITIAL REVISIONS ====================
./manage.py createinitialrevisions
echo ===================== COLLECTING STATIC FILES ======================
./manage.py collectstatic --noinput
touch main/wsgi.py
deactivate
