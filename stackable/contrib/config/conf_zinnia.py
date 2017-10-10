from stackable.stackable import StackableSettings


class Config_DjangoBlogZinnia(object):
    # http://docs.django-blog-zinnia.com/en/develop/getting-started/install.html
    _apps_ = (
        'django_comments',
        'tagging',
        'zinnia',
        'cmsplugin_zinnia'
    )
    __patches__ = (
        StackableSettings.patch_apps(_apps_),
    )
