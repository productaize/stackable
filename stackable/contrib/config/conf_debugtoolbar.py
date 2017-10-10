from stackable.stackable import EnvSettingsBase


class Config_DebugToolbar(object):
    # django debug toolbar, see github.com/django-debug-toolbar
    _apps_ = ('debug_toolbar', 'django.contrib.admin')
    _mw_ = ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    __patches__ = (
        EnvSettingsBase.patch_apps(_apps_),
        EnvSettingsBase.patch_middleware(_mw_, prepend=True),
    )
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
