import os

from stackable import StackableSettings


def patch_context_processors(configs):
    # Django > 1.8 compat
    if 'TEMPLATES' in configs:
        ctx_procs = configs['TEMPLATES'][0]['OPTIONS']['context_processors']
        for proc in configs['TEMPLATE_CONTEXT_PROCESSORS']:
            ctx_procs.append(proc) if proc not in ctx_procs else None
        del configs['TEMPLATE_CONTEXT_PROCESSORS']


class Config_DjangoGrappelli:
    # adopted from https: // django - grappelli.readthedocs.io / en / latest / quickstart.html  # installation

    _addl_apps = ('grappelli',)

    TEMPLATE_CONTEXT_PROCESSORS = [
        'django.template.context_processors.request',
    ]

    GRAPPELLI_ADMIN_TITLE = os.environ.get('DJANGO_ADMIN_TITLE', 'landingpage admin')

    StackableSettings.patch_apps(_addl_apps, prepend=True, at='django.contrib.admin')
    StackableSettings.patch_func(patch_context_processors, tuple())
