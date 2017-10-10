from stackable.stackable import StackableSettings


class Config_Swagger(object):
    _addl_apps_ = (
        'tastypie_swagger',
    )
    __patches__ = (
        StackableSettings.patch_apps(_addl_apps_),
    )
