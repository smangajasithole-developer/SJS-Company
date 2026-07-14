#!/bin/bash

python manage.py migrate --settings=myProject.settings.production
python manage.py collectstatic --noinput --settings=myProject.settings.production