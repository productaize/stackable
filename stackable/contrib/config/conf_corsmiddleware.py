from __builtin__ import False

from stackable.stackable import StackableSettings


class Config_DjangoCorsMiddleware(object):
    _apps_ = (
        'corsheaders',
    )
    _mw_ = (
        'corsheaders.middleware.CorsMiddleware',
    )
    __patches__ = (
        StackableSettings.patch_apps(_apps_),
        StackableSettings.patch_middleware(
            _mw_, prepend=True, at='django.middleware.common.CommonMiddleware')
    )
    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_WHITELIST = ()  # tuple of 'host:port' format
    CORS_ORIGIN_REGEX_WHITELIST = ()
    CORS_URLS_REGEX = r'^/api/.*$'
    CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    )
    CORS_ALLOW_HEADERS = (
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken'
    )
    CORS_EXPOSE_HEADERS = ()
    CORS_ALLOW_CREDENTIALS = True  # True for sessions with cookies
    CORS_REPLACE_HTTPS_REFERER = False
    CORS_URLS_ALLOW_ALL_REGEX = ()
