class Config_AsyncEmail(object):
    # configure celery email backend for async email
    # https://pypi.python.org/pypi/django-celery-email
    EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
    CELERY_EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
    MAILGUN_ACCESS_KEY = 'gggggggggggggggggggggggggggggggggggg'
    MAILGUN_SERVER_NAME = 'shrebo.mailgun.org'
