from stackable.stackable import StackableSettings


def patchdb(settings, *args, **kwargs):
    """ update databases from settings """
    db = settings['DATABASES']
    db['default']['DB_DUMP_EMPTY_TABLES'] = settings.get(
        'DB_DUMP_EMPTY_TABLES', [])
    db['default']['DB_DUMP_EXCLUDED_TABLES'] = settings.get(
        'DB_DUMP_EXCLUDED_TABLES', [])


class Config_DbDump(object):
    # config for https://github.com/vitaliyf/django-dbdump
    _addl_apps_ = (
        'dbdump',
    )
    __patches__ = (
        StackableSettings.patch_apps(_addl_apps_),
        StackableSettings.patch(patchdb)
    )
    # add these to your local config
    DB_DUMP_EMPTY_TABLES = []
    DB_DUMP_EXCLUDED_TABLES = []
