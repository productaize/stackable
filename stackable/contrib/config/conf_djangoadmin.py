from stackable.stackable import StackableSettings


class hashabledict(dict):

    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class hashablelist(list):

    def __hash__(self):
        return hash(tuple(sorted(self)))


class Config_DjangoAdmin(object):
    # https://docs.djangoproject.com/en/1.11/ref/contrib/admin/
    _add_apps = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.messages',
        'django.contrib.sessions',
    )

    _add_mw = (
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    _ctxp_append = (
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    )

    StackableSettings.patch_list(
        'TEMPLATE_CONTEXT_PROCESSORS', _ctxp_append)
    StackableSettings.patch_apps(_add_apps)
    StackableSettings.patch_middleware(_add_mw)
