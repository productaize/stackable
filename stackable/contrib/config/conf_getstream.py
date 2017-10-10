'''
Created on Oct 26, 2015

@author: @gaumire
'''
from stackable.stackable import EnvSettingsBase


class Config_GetStream(object):

    _additional_apps_ = (
        'stream_django',
    )
    __patches__ = (
        EnvSettingsBase.patch_apps(_additional_apps_),
    )
    STREAM_API_KEY = 'invalid key'
    STREAM_API_SECRET = 'invalid key'
