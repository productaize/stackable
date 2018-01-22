import os

from stackable.stackable import StackableSettings


class Config_DjangoWhitenoise(object):

    """
    whitenoise configuration
    @see https://pypi.python.org/pypi/whitenoise#infrequently-asked-questions
    """
    # enable for persisent file and gzip support
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    if os.environ.get('DJANGO_STATIC'):
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

    _addl_mware = ('whitenoise.middleware.WhiteNoiseMiddleware',)
    StackableSettings.patch_middleware(_addl_mware)
