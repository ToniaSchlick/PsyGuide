"""
WSGI config for PsyGuideSite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PsyGuideSite.settings")

os.environ['DJANGO_SETTINGS_MODULE'] = 'PsyGuideSite.settings'
export DJANGO_SETTINGS_MODULE=mysite.settings
settings.configure()
if not settings.configured:
    settings.configure(myapp_defaults, DEBUG=True)

application = get_wsgi_application()
