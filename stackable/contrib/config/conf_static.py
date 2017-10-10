import os


class Config_StaticFiles(object):
    # static files
    BASE_DIR = '/tmp'
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"
