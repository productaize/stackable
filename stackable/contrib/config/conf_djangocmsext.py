'''
Created on Sept 23, 2015

@author: Gaurav Ghimire
'''
import os

from stackable.stackable import StackableSettings

from stackable.contrib.conf_cmscascade import Config_DjangoCMSCascade
class Config_DjangoCMSExtended(Config_DjangoCMSCascade):

    """ 
    more CMS plugins

    configuration for Django CMS 3.2.5 with Django 1.7 
    """
    additional_apps = (
        'djangocms_snippet',
        'cmsplugin_filer_file',
        'cmsplugin_filer_link',
        'cmsplugin_filer_folder',
        'cmsplugin_filer_image',
        'cmsplugin_filer_teaser',
        'cmsplugin_filer_video',
        # -- end of forms builder
        'easy_thumbnails',
        'filer',
        's3_folder_storage',
        # -- start forms builder
        # -- removed as not working properly @ 1.0.1
        #'cmsplugin_forms_builder',
        #'forms_builder.forms',
        # 'bootstrap3', # required for forms_builder
        'aldryn_background_image',
    )

    _caches_ = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'django_db_cache',
        }
    }

    __migration_modules__ = {
        'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
        'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
        'cmsplugin_filer_link': 'cmsplugin_filer_link.migrations_django',
        'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
        'cmsplugin_filer_teaser': 'cmsplugin_filer_teaser.migrations_django',
        'cmsplugin_filer_video': 'cmsplugin_filer_video.migrations_django',
    }

    __patches__ = (
        StackableSettings.patch_apps(additional_apps),
        StackableSettings.patch_dict('MIGRATION_MODULES',
                                     __migration_modules__),
        StackableSettings.patch_dict('CACHES', _caches_),
    )

    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        #'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    )

    CMSPLUGIN_CASCADE_PLUGINS = ('cmsplugin_cascade.bootstrap3',)

    DJANGOCMS_YOUTUBE_API_KEY = os.environ.get('DJANGOCMS_YOUTUBE_API_KEY', '')
