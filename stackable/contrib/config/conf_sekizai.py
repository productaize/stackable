from stackable.stackable import StackableSettings

def patch_context_processors(configs):
    # Django > 1.8 compat
    if 'TEMPLATES' in configs:
        ctx_procs = configs['TEMPLATES'][0]['OPTIONS']['context_processors']
        ctx_procs.extend(configs['TEMPLATE_CONTEXT_PROCESSORS'])
        del configs['TEMPLATE_CONTEXT_PROCESSORS']

class Config_DjangoSekizai(object):
    _add_app = (
        'sekizai',
    )

    _ctxp_append = (
        'django.template.context_processors.media',
        'django.template.context_processors.static',
        'sekizai.context_processors.sekizai',
    )

    StackableSettings.patch_apps(_add_app)
    StackableSettings.patch_list('TEMPLATE_CONTEXT_PROCESSORS', _ctxp_append)
    StackableSettings.patch_func(patch_context_processors, tuple())
