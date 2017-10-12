class Config_SyncEmail(object):
    # configure celery email backend for async email
    # https://pypi.python.org/pypi/django-celery-email
    EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
    MAILGUN_ACCESS_KEY = 'gggggggggggggggggggggggggggggggggggg'
    MAILGUN_SERVER_NAME = 'shrebo.mailgun.org'