from stackable.stackable import StackableSettings



class Config_Bootstrap3(object):
    _addl_apps = (
        'bootstrap3',
    )

    StackableSettings.patch_apps(_addl_apps)
