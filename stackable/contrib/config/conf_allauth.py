'''
Created on Dec 19, 2014

@author: patrick
'''
import six
from stackable.stackable import EnvSettingsBase
ALLAUTH_PROVIDERS = {
    'twitter': 'allauth.socialaccount.providers.twitter',
    'google': 'allauth.socialaccount.providers.google',
    'facebook': 'allauth.socialaccount.providers.facebook',
}


def conditional_accounts(settings, *args, **kwargs):
    """
    enable social accounts as specified in SOCIAL_ACCOUNTS_ENABLED

    SOCIAL_ACCOUNTS_ENABLED is either

    * a tuple or list of social accounts (twitter, google, facebook)
    * a string with comma separated list of social accounts

    The providers must be allauth socialaccount provider classes. You
    may override the default ALLAUTH_PROVIDERS in your settings. The
    default has entries for twitter, google, facebook.

    Be sure to include the following url:

    # urls.py
    urlpatterns += [url(r'^accounts/', include('allauth.urls'))]
    """
    apps = list(settings['INSTALLED_APPS'])
    social_apps = settings.get('SOCIAL_ACCOUNTS_ENABLED', [])
    providers = settings.get('ALLAUTH_PROVIDERS', ALLAUTH_PROVIDERS)
    if isinstance(social_apps, six.string_types):
        social_apps = social_apps.split(',')
    for app in social_apps:
        apps.append(providers[app])
    settings['INSTALLED_APPS'] = tuple(apps)


class Config_DjangoAllAuth(object):
    allauth_apps_append = (
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
    )
    allauth_ab_append = (
        'allauth.account.auth_backends.AuthenticationBackend',

    )
    allauth_south_migration = {
        'account': 'ignore',
    }

    __patches__ = (
        EnvSettingsBase.patch_apps(allauth_apps_append),
        EnvSettingsBase.patch_list(
            'AUTHENTICATION_BACKENDS', allauth_ab_append),
        EnvSettingsBase.patch_dict(
            'SOUTH_MIGRATION_MODULES', allauth_south_migration),
        EnvSettingsBase.patch(
            conditional_accounts),
    )
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 5
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False
    SOCIALACCOUNT_QUERY_EMAIL = True
