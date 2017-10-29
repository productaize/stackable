import argparse
import json
import os
from uuid import uuid4

import yaml

from .crypto import AESCipher


def siteenv(site=None, envclass='EnvSettings_Local', api_password=None,
            keysfile=None, plain=False, env_var=None):
    """
    print the site environment variables for deployment
    """
    site = site or os.path.basename(os.path.dirname(__file__))
    keysfile = keysfile or os.path.expanduser('~/.stackable/keys.yml')
    print "Creating variables for %s from %s" % (site, keysfile)
    api_password = "%s" % uuid4() or os.environ.get('ENV_APIKEY_DECRYPT')
    with open(keysfile, 'r') as f:
        # load cleartext keys and config settings from yml file
        keys = yaml.load(f)
        e_settings = keys.get(envclass, None)
        if e_settings is None:
            print "[WARN] Cannot find any keys for %s" % envclass
            exit()
        if env_var is not None:
            # prints the variable value
            print "%s=%s" % (env_var, e_settings[env_var])
            exit()
        # create encrypted key file per environment
        aes = AESCipher(api_password)
        keyenvvar = '%s_KEYS' % envclass
        cleartext = json.dumps(e_settings)
        ciphertext = aes.encrypt(cleartext)
    envvars = [
        'DJANGO_CONFIGURATION=%s' % envclass,
        'DJANGO_CONFIGURATION_TEST=%s' % envclass,
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

parser = argparse.ArgumentParser(description='stackable key encryption')
parser.add_argument('--keysfile', help='/path/to/keys.yml, defaults to ~/.stackable/keys.yml')
parser.add_argument('--envclass', help='environment class name, defaults to EnvSettings_Local')

args = parser.parse_args()

if __name__ == '__main__':
    siteenv(**vars(args))
