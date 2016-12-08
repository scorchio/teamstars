"""
WSGI config for teamstars project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""
import sys
import os
from django.core.wsgi import get_wsgi_application

sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", ".settings")

application = get_wsgi_application()
