from stackable.stackable import StackableSettings
class Config_Axes(object):
    """
    django-axes 
    
    https://pypi.python.org/pypi/django-axes
    """
    _apps_ = ('axes',)

    __patches__ = (
        StackableSettings.patch_apps(_apps_),
    )
