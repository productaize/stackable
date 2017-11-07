from stackable.stackable import StackableSettings


class Config_DjangoConstance(object):
    # https://django-constance.readthedocs.io/en/latest/index.html#
    _add_apps = ('constance',
                 'constance.backends.database',)

    CONSTANCE_CONFIG = {
        'THE_ANSWER': (42, 'Answer to the Ultimate Question of Life, '
                       'The Universe, and Everything'),
    }

    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
    #CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

    StackableSettings.patch_apps(_add_apps)
