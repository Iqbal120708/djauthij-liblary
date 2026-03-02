from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

APP_NAME = getattr(settings, "ACCOUNTS_APP_NAME", "DJ Auth")

try:
    EMAIL_HOST_USER = settings.EMAIL_HOST_USER
except AttributeError:
    raise ImproperlyConfigured("EMAIL_HOST_USER is not set in settings.py")