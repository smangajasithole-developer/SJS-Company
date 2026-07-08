#!/bin/bash

python manage.py collectstatic --noinput --settings=myProject.settings.production
