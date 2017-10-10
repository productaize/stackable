'''
Created on Oct 28, 2013

@author: patrick
'''
from stackable.stackable import EnvSettingsBase


class Config_SiteHttps(object):

    """
    A configuration mix in to enable full site encryption
    Overred the SECURE_REQUIRED_PATHS to set sub-site paths only

    MAKE SURE YOU LIST THE MIXIN *BEFORE* THE PARENT CLASS, e.g.

    NOTE: This overrides the MIDDLEWARE_CLASSES. To preserve
    adjustments higher up the hierarchy, use:

    MIDDLEWARE_CLASSES = SSL_MIDDLEWARE_CLASSES
    MIDDLEWARE_CLASSES += MyParentClass.MIDDLEWARE_CLASSES

    class MySettings(Config_SiteHttps, MyGlobalSettings):
      pass
    """
    # setup the middle ware. Secure middle ware must be in the
    # beginning!
    # set the paths to be secured -- defaults to all requests
    HTTPS_SUPPORT = True
    SECURE_REQUIRED_PATHS = ('*',)
    SSL_MIDDLEWARE_CLASSES = []
    # config patches to be applied
    __patches__ = (
        EnvSettingsBase.patch_middleware(
            SSL_MIDDLEWARE_CLASSES, prepend=False, remove=False),
    )
