'''
Created on Oct 27, 2014

@author: patrick
'''
from stackable.stackable import EnvSettingsBase


class Config_DjangoGuardian(object):
    # see http://django-guardian.readthedocs.org/en/v1.2/configuration.html
    apps_append = ('guardian',)
    auth_backends_append = ('guardian.backends.ObjectPermissionBackend',)

    __patches__ = (
        EnvSettingsBase.patch_list('AUTHENTICATION_BACKENDS',
                                   auth_backends_append),
        EnvSettingsBase.patch_apps(apps_append),
    )

    ANONYMOUS_USER_ID = -1
