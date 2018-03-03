from stackable.stackable import StackableSettings


class Config_DjangoNoseTests(object):
    _addl_apps = (
        'django_nose',
    )
    StackableSettings.patch_apps(_addl_apps)
    
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
