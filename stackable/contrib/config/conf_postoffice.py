from stackable.stackable import EnvSettingsBase


def setup_postoffice(globals, *args):
    """ this runs post any other email settings,
    so we can safely reconfigure post office to
    match whatever other email backend was set """
    # get post office config
    po_config = globals['POST_OFFICE']
    # get the current email backend w/o post office
    backend = globals['EMAIL_BACKEND']
    # ... set this as post office backend
    po_config['EMAIL_BACKEND'] = backend
    # finally, make post office the email backend
    globals['EMAIL_BACKEND'] = 'post_office.EmailBackend'


class Config_DjangoPostOffice(object):
    """
    set up django-post-office
    @see https://github.com/miraculixx/django-post_office
    """
    _apps_ = (
        'post_office',
    )
    POST_OFFICE_CACHE = False
    POST_OFFICE_TEMPLATE_CACHE = False
    #     _caches_ = {
    #        'post_office': {
    #         'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
    #         'LOCATION': '127.0.0.1:11211',
    #        }
    #     }
    POST_OFFICE = {
        'EMAIL_BACKEND': '=>will be set in patch, setup_postoffice',
        'BATCH_SIZE': 1,
        'DEFAULT_PRIORITY': 'now',  # now, low, medium, high, now = sync
        'LOG_LEVEL': 1,  # 0 = nothing, 1 = only failed, 2 = both
        'SENDING_ORDER': ['created'],
        # specify serializer for context variables for deferred rendering
        # (render_on_delivery=True)
        # 'CONTEXT_FIELD_CLASS': 'picklefield.fields.PickledObjectField',

    }
    __patches__ = (
        EnvSettingsBase.patch_apps(_apps_),
        # EnvSettingsBase.patch_dict('CACHES', _caches_),
        EnvSettingsBase.patch(setup_postoffice),
    )
