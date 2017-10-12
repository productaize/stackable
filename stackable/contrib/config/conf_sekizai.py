from stackable.stackable import StackableSettings


class Config_DjangoSekizai(object):
    _add_app = (
        'sekizai',
    )

    _ctxp_append = (
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'sekizai.context_processors.sekizai',
    )

    StackableSettings.patch_apps(_add_app)
    StackableSettings.patch_list(
        'TEMPLATE_CONTEXT_PROCESSORS', _ctxp_append)
