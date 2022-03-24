class Config_TeamcityTests:
    # use this to have PyCharm integration for Django tests
    try:
        import teamcity
        TEST_RUNNER = "teamcity.django.TeamcityDjangoRunner"
    except ModuleNotFoundError:
        pass
