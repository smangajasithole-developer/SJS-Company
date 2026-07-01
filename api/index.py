import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "myProject.settings.production"
)

from myProject.wsgi import application

def handler(request, context):
    return application(request, context)