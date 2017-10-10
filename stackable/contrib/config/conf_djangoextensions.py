from stackable.stackable import StackableSettings


def patch_logger(globals, *args, **kwargs):
    LOGGING = globals.get('LOGGING')
    LOGGING['loggers']['werkzeug'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    }


class Config_DjangoExtensions(object):
    # werkzeug debugger for runserver_plus
    # http://django-extensions.readthedocs.io/en/latest/runserver_plus.html
    WERKZEUG_DEBUG_PIN = 'off'

    _apps_ = ('django_extensions',)

    __patches__ = (
        StackableSettings.patch(patch_logger),
        StackableSettings.patch_apps(_apps_),
    )
