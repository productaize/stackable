'''
Created on Jan 13, 2015

@author: patrick
'''
from stackable.stackable import StackableSettings


class Config_ModelTranslation(object):
    # http://django-modeltranslation.readthedocs.org/en/latest/installation.html#setup
    USE_I18N = True
    MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
    _apps_ = (
        'modeltranslation',
    )
    __patches__ = (
        StackableSettings.patch_apps(_apps_, prepend=True,
                                     at='django.contrib.admin'),
    )
    # fix "'Country' object has no attribute 'name_ascii_en'"
    # https://bitbucket.org/neithere/django-autoslug/issues/42/setting-to-enable-disable-modeltranslation
    AUTOSLUG_MODELTRANSLATION_ENABLE = False
