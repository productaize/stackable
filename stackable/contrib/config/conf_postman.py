from stackable.stackable import StackableSettings


class Config_DjangoPostman(object):
    # http://django-postman.readthedocs.org/
    _addl_apps_ = (
        'postman',
    )
    __patches__ = (
        StackableSettings.patch_apps(_addl_apps_),
    )
    POSTMAN_AUTO_MODERATE_AS = True
