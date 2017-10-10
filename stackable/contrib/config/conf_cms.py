'''
Created on Sep 17, 2014

@author: patrick
'''
from stackable.stackable import EnvSettingsBase


class Config_DjangoCMS(object):

    """
    basic working setup for django

    configuration for Django CMS 3.2.5 with Django 1.7
    """

    cms_apps_prepend_1 = (
        'djangocms_admin_style',
    )
    cms_apps_prepend_2 = (
        'djangocms_text_ckeditor',
    )
    cms_apps_append = (
        'djangocms_picture',
        'djangocms_style',
        'djangocms_googlemap',
        'menus',
        'sekizai',
        'cms',
        'treebeard',
    )
    cms_mw_append = (
        'cms.middleware.user.CurrentUserMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.toolbar.ToolbarMiddleware',
        'cms.middleware.language.LanguageCookieMiddleware',
        'cms.middleware.utils.ApphookReloadMiddleware',
    )
    cms_mw_insert_before_common = (
        'django.middleware.doc.XViewMiddleware',
    )
    cms_ctxp_insert = (
        'django.core.context_processors.i18n',
    )
    cms_ctxp_append = (
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.static',
        'sekizai.context_processors.sekizai',
        'cms.context_processors.cms_settings',
    )
    # apply settings patches
    __patches__ = (
        EnvSettingsBase.patch_apps(cms_apps_prepend_1, prepend=True,
                                   at='django.contrib.admin'),
        EnvSettingsBase.patch_apps(cms_apps_prepend_2, prepend=False,
                                   at='django.contrib.admin'),
        EnvSettingsBase.patch_apps(cms_apps_append),
        EnvSettingsBase.patch_middleware(cms_mw_append),
        EnvSettingsBase.patch_middleware(
            cms_mw_insert_before_common, at='django.middleware.locale.LocaleMiddleware'),
        EnvSettingsBase.patch_list('TEMPLATE_CONTEXT_PROCESSORS',
                                   cms_ctxp_insert,
                                   at='django.contrib.messages.context_processors.messages'),
        EnvSettingsBase.patch_list(
            'TEMPLATE_CONTEXT_PROCESSORS', cms_ctxp_append)
    )
    # other CMS settings
    CMS_TEMPLATES = (
        ('dashboard/index.html', 'Dashboard'),
        ('home.html', 'Home'),
        ('cms/base.html', 'Base page'),
    )
    CMS_PERMISSION = True
