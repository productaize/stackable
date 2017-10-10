import os


class Config_AWS(object):
    # filedepot and django-extension's s3_sync setup. see settings.py
    # for filedepot configuration
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET_NAME = os.environ.get('AWS_TEST_BUCKET')
    # http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
    AWS_DEFAULT_ACL = 'private'
    AWS_BUCKET_ACL = 'private'
