'''
Created on Oct 27, 2013

@author: patrick
'''
import os

from stackable.stackable import EnvSettingsBase

from .conf_fullhttps import Config_SiteHttps


class EnvSettings_admin(Config_SiteHttps):

    """
    PRODUCTION SITE SETTINGS. 

    TO PROTECT ALL PATHS WITH HTTPS:

    * SESSION_COOKIE_SECURE = True
    * CSRF_COOKIE_SECURE = True
    * SECURE_REQUIRED_PATHS = ('*',)

    TO PROTECT ONLY SPECIFIC PATHS:

    * SESSION_COOKIE_SECURE = False
    * CSRF_COOKIE_SECURE = False
    * SECURE_REQUIRED_PATHS = ('/uri/path', '/uri/path',)

    """
    DEBUG = False
    ENABLE_ADMIN = True
    _apps_additions_ = ('django.contrib.admin',)
    EnvSettingsBase.patch_apps(_apps_additions_,
                               after='django.contrib.sitemaps')
    # HTTPS
    # see http://security.stackexchange.com/questions/8964/trying-to-make-a-django-based-site-use-https-only-not-sure-if-its-secure
    # SESSION_COOKIE_SECURE=True
    # CSRF_COOKIE_SECURE=True
    SECURE_REQUIRED_PATHS = ('/accounts/', '/profile/', '/admin/', )
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    # make sure we get the secret key from outside so it only lives in memory
    # never on disk
    SECRET_KEY = os.environ.get('DJANGO_PROB_SEED', "")
    # haystack
    ES_INDEX_NAME = "haystack"
