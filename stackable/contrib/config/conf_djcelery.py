import multiprocessing
import os

from stackable.stackable import EnvSettingsBase


def concurrency():
    return multiprocessing.cpu_count()


def patch_logging(_globals, _logging_):
    logging = _globals.get('LOGGING')
    loggers = logging['loggers']
    loggers.update(_logging_)


class Config_DjangoCelery(object):
    _addl_apps_ = ('djcelery',)
    _logging_ = {
        'celery.worker': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
    CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
    CELERY_CACHE_BACKEND = 'djcelery.backends.cache:DatabaseBackend'
    CELERY_ACCEPT_CONTENT = ['pickle']
    CELERY_ACCEPT_CONTENT = ['pickle']
    CELERY_TASK_SERIALIZER = 'pickle'
    CELERY_RESULT_SERIALIZER = 'pickle'
    CELERY_REDIRECT_STDOUTS = False
    CELERY_REDIRECT_STDOUTS_LEVEL = 'debug'
    CELERY_SEND_EVENTS = True
    BROKER_HEARTBEAT = os.environ.get('CELERY_HEARTBEAT', 5)
    CELERYD_CONCURRENCY = os.environ.get('WORKER_CONCURRENCY', concurrency())
    BROKER_URL = 'amqp://guest@127.0.0.1:5672//'
    __patches__ = (
        EnvSettingsBase.patch_apps(_addl_apps_),
        EnvSettingsBase.patch(patch_logging, _logging_)
    )
