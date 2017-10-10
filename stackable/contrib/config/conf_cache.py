from django.db.models.signals import post_migrate
from django.dispatch.dispatcher import receiver
from stackable.stackable import StackableSettings


def create_cache_table(table_name):
    """
    safely create the cache table 
    """
    from django.db import connection
    cursor = connection.cursor()
    sql = """
     CREATE TABLE IF NOT EXISTS `{table_name}` (
      `cache_key` varchar(255) NOT NULL,
      `value` longtext NOT NULL,
      `expires` datetime NOT NULL,
      PRIMARY KEY (`cache_key`),
      KEY `django_db_cache_expires` (`expires`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    try:
        cursor.execute(sql.format(table_name=table_name))
    except Warning:
        # mysql warns about already existing table. we don't care
        pass


def setup_cache_table(settings, *args, **kwargs):
    """
    process all CACHES configs and create tables for database backend
    """
    CACHES = settings.get('CACHES')
    # create all cache tables
    for name, config in CACHES.iteritems():
        if 'db.DatabaseCache' in config.get('BACKEND', ''):
            table_name = config['LOCATION']
            create_cache_table(table_name)


class Config_DjangoCacheDB(object):
    # db cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            # cache table, create in setup_cache_table patch
            'LOCATION': 'django_db_cache',
        }
    }
    # setup cache table
    __patches__ = (
        StackableSettings.patch(setup_cache_table),
    )


@receiver(post_migrate)
def post_migrate_create_cache(*args, **kwargs):
    from django.conf import settings
    setup_cache_table({'CACHES': settings.CACHES})
