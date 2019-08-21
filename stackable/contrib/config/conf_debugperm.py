from stackable import StackableSettings


class Config_DjangoDebugPermissions:
    # https://github.com/timonweb/django-debug-permissions
    _add_apps = ('debug_permissions',)

    StackableSettings.patch_apps(_add_apps)
