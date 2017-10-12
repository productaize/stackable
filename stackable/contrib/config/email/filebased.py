class Config_FileEmail(object):
    # configure celery email backend for sync email
    # https://pypi.python.org/pypi/django-celery-email
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = './tmp/app-messages' 
