
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

    def update(self, *args, **kwargs):
        # ignore any updates
        pass


class Config_DisableMigrations():
    MIGRATION_MODULES = DisableMigrations()
