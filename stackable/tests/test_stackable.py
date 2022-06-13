from io import StringIO

import os
from unittest.case import TestCase


from stackable import stackable
from stackable.contrib.config.conf_api import Config_ApiKeys
from stackable.encryptkeys import siteenv


class TestConfig(Config_ApiKeys):
    FOO = 'secret'


class StackableTests(TestCase):

    def setUp(self):
        TestCase.setUp(self)

    def tearDown(self):
        TestCase.tearDown(self)

    def test_environment_keys(self):
        # provide a 'secret' keys file and encrypt it
        keysfile = StringIO("""
        TestConfig:
           FOO: bar
        """)
        envvars, password = siteenv(envclass='TestConfig',
                                    keysfile=keysfile,
                                    plain=True, silent=True)
        # update environment with encrypted variable
        environ = os.environ
        environ['ENV_APIKEY_DECRYPT'] = password
        for var_value in envvars:
            var, value = var_value.split('=', 1)
            environ[var] = value
        # attempt instantiating TestConfig, overriding its values
        # from the secret key
        globalsobj = {}
        stackable.EnvSettingsBase.setup(globalsobj, env_class='TestConfig',
                                        config_mod='stackable.tests')
        self.assertEqual(globalsobj['FOO'], 'bar')
