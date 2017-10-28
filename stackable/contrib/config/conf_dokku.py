import os

from stackable.stackable import EnvSettingsBase, StackableSettings

import dj_database_url


def patch_db(globals):
    DATABASES = globals['DATABASES']
    if os.environ.get('MYSQL_URL'):
        DATABASES['default'].update(dj_database_url.config('MYSQL_URL'))
    elif os.environ.get('DATABASE_URL'):
        DATABASES['default'].update(dj_database_url.config('DATABASE_URL'))


class Config_Dokku(object):
    StackableSettings.patch(patch_db)
    TMP_FOLDER = '/tmp'
    # for compatibility with both dokku version 0.3.x and 0.4.x
    if not os.environ.get('RABBITMQ_URL'):
        BROKER_USERNAME = os.environ.get('BROKER_USERNAME', "guest")
        BROKER_PASSWORD = os.environ.get('BROKER_PASSWORD', "")
        BROKER_PORT_5672_TCP_ADDR = os.environ.get(
            'BROKER_PORT_5672_TCP_ADDR', "localhost")
        BROKER_PORT_5672_TCP_PORT = os.environ.get(
            'BROKER_PORT_5672_TCP_PORT', "5672")

        BROKER_OPTS = dict(user=BROKER_USERNAME,
                           password=BROKER_PASSWORD,
                           addr=BROKER_PORT_5672_TCP_ADDR,
                           port=BROKER_PORT_5672_TCP_PORT)

        BROKER_URL = "amqp://{user}:{password}@{addr}:{port}//".format(
            **BROKER_OPTS)
    else:
        BROKER_URL = os.environ.get('RABBITMQ_URL')

    REDIS_URL = os.environ.get('REDIS_URL')
    # MONGODB_URL = os.environ.get('MONGOHQ_URL')
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CLIENTAPP_PING_RUNVAR = 'HOSTNAME'
