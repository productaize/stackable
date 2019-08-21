
class DisableMigrations(object):

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

    def update(self, args: object, kwargs: object) -> object:
        """

        :rtype: 
        """
        # ignore any updates
        pass


class Config_DisableMigrations():
    MIGRATION_MODULES = DisableMigrations()
