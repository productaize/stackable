from stackable.stackable import StackableSettings


class Config_Celery(object):

    """
    basic celery configuration
    """
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
    BROKER_URL = 'amqp://guest@127.0.0.1:5672//'
    CELERY_RESULT_BACKEND = 'amqp'

    _apps_ = ('djcelery',)

    __patches__ = (
        StackableSettings.patch_apps(_apps_),
    )
