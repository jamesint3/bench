#!/usr/bin/env sh
set -eu

python gexable_esg/apps/django_project/scripts/wait_for_db.py
python gexable_esg/apps/django_project/manage.py migrate users
python gexable_esg/apps/django_project/manage.py migrate --run-syncdb
python gexable_esg/apps/django_project/manage.py apply_sql_artifacts
python gexable_esg/apps/django_project/manage.py runserver 0.0.0.0:8000
