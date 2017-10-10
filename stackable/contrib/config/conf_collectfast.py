from stackable.stackable import StackableSettings


def update_cache(settings, *args, **kwargs):
    CACHES = settings.get('CACHES')
    CACHES['collectfast'] = {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'collectfast_cache',
    }


class Config_Collectfast(object):
    _apps_ = ('collectfast',)
    __patches__ = (
        StackableSettings.patch(update_cache),
        StackableSettings.patch_apps(
            _apps_, prepend=True, at='django.contrib.staticfiles')
    )
    COLLECTFAST_CACHE = 'collectfast'
    AWS_PRELOAD_METADATA = True
