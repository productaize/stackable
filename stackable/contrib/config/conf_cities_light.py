'''
Created on Oct 9, 2014

@author: patrick
'''
from stackable.stackable import EnvSettingsBase


class Config_Cities_Light(object):
    # see https://github.com/jazzband/django-cities-light
    apps_append = (
        'cities_light',
    )
    __patches__ = (
        EnvSettingsBase.patch_apps(apps_append),
    )

    CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en']
    CITIES_LIGHT_INCLUDE_COUNTRIES = ['CH']
