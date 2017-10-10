'''
Created on Oct 9, 2014

@author: patrick
'''
from stackable.stackable import EnvSettingsBase


class Config_Cities_Light(object):
    apps_append = (
        'cities_light',
    )
    __patches__ = (
        EnvSettingsBase.patch_apps(apps_append),
    )

    CITIES_LIGHT_INCLUDE_COUNTRIES = ['CH']
