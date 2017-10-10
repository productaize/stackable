from stackable.stackable import StackableSettings


def patch_formats(settings, *args, **kwargs):
    # fix a bug introduced in Django 1.7.11
    # https://github.com/django/django/commit/8a01c6b53169ee079cb21ac5919fdafcc8c5e172
    # compare to Django 1.8
    # https://github.com/django/django/commit/9582ba51bd486c5785c0e76ed7f7996119bc9650
    # TODO remove once we are at Django >= 1.8 and have migrated to
    # using format modules
    try:
        from django.utils import formats
        _formats = list(getattr(formats, 'FORMAT_SETTINGS'))
    except:
        pass
    else:
        _formats.append('SHREBO_DATETIME_FORMAT')
        setattr(formats, 'FORMAT_SETTINGS', frozenset(_formats))


class Config_DjangoFormats(object):
    __patches__ = (
        StackableSettings.patch(patch_formats),
    )
    SHREBO_DATETIME_FORMAT = "d.m.Y H:i"
