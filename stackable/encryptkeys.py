import json
import os
from uuid import uuid4

import yaml

from .crypto import AESCipher


def siteenv(site=None, env_class='EnvSettings_Local', api_password=None,
            keysfile=None, plain=False, env_var=None):
    """
    print the site environment variables for deployment
    """
    site = site or os.path.basename(os.path.dirname(__file__))
    keysfile = os.path.expanduser('~/.stackable/keys.yml')
    print "Creating variables for %s from %s" % (site, keysfile)
    api_password = "%s" % uuid4() or os.environ.get('ENV_APIKEY_DECRYPT')
    with open(keysfile, 'r') as f:
        # load cleartext keys and config settings from yml file
        keys = yaml.load(f)
        e_settings = keys.get(env_class, None)
        if e_settings is None:
            print "[WARN] Cannot find any keys for %s" % env_class
            exit()
        if env_var is not None:
            # prints the variable value
            print "%s=%s" % (env_var, e_settings[env_var])
            exit()
        # create encrypted key file per environment
        aes = AESCipher(api_password)
        keyenvvar = '%s_KEYS' % env_class
        cleartext = json.dumps(e_settings)
        ciphertext = aes.encrypt(cleartext)
    envvars = [
        'DJANGO_CONFIGURATION=%s' % env_class,
        'DJANGO_CONFIGURATION_TEST=%s' % env_class,
        'ENV_APIKEY_DECRYPT=%s' % api_password,
        '%s=%s' % (keyenvvar, ciphertext.replace('\n', '')),
    ]
    if not plain:
        # show a little help
        print "Set the environment for %s as follows:" % site
        print '---'
        print "export", " ".join(envvars)
    else:
        print "\n".join(envvars)


if __name__ == '__main__':
    siteenv()