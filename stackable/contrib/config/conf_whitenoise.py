import os


class Config_DjangoWhitenoise(object):
    """
    whitenoise configuration
    @see https://pypi.python.org/pypi/whitenoise#infrequently-asked-questions
    """
    # enable for persisent file and gzip support
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
    if os.environ.get('DJANGO_STATIC'):
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
