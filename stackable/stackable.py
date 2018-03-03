'''
Created on Oct 27, 2013

@author: patrick
'''
from __future__ import print_function

from importlib import import_module
import inspect
import json
import logging
import os
import sys

from ordered_set import OrderedSet
from six import string_types, iteritems

from .crypto import AESCipher
logger = logging.getLogger(__name__)
_PATCHES = []
_CONFIG_MODULES = []


def password():
    # try to get a password from ENV_APIKEY_DECRYPT
    # if successful create AESCipher instance else leave password blank
    # if password is blank we will not decrypt keys in setup() method
    password = ''
    aes = None
    try:
        password = os.environ['ENV_APIKEY_DECRYPT']
    except KeyError:
        pass
    else:
        aes = AESCipher(password)
    return password, aes


class EnvSettingsBase(object):

    """
    Setup environment specific settings variables. This will
    get all UPPERCASE class variables from the specified class
    into the module-level variables in settings.

    Use in settings.py:

    a) EnvSettingsBase.setup(globals(), "MyEnvSettings_classname")
    b) EnvSettingsBase.setup(globals(), os.environ['DJANGO_CONFIGURATION'])
    c) EnvSettingsBase.setup(globals(), os.environ['DJANGO_CONFIGURATION'], 
       ("config_module_name", ...))
    The default config module is "config"
    """

    _patches = _PATCHES
    _config_modules = _CONFIG_MODULES
    verbose = False
    # settings allowed to patch after keys were applied
    _allow_keys_patch = []

    @classmethod
    def setup(cls, globalsobj, env_class=None, config_mod=("config",),
              silent=False, use_lowercase=False):
        cls.password, cls.aes = password()
        if isinstance(env_class, string_types):
            if '.' in env_class:
                config_mod = env_class.split('.')[:-1]
                env_class = env_class.split('.')[-1]
        cls.info("[INFO] Loading configuration %s using %s" %
                 (env_class, config_mod))
        # make sure we have tuples as input
        env_class = make_tuple(env_class)
        config_mod = make_tuple(config_mod)
        # apply all configs in all modules requested
        globalsobj['SETTINGS_PATCHES_APPLIED'] = []
        globalsobj['SETTINGS_APPLIED'] = []
        for cm in config_mod:
            for ec in env_class:
                cls.apply_config(globalsobj, env_class=ec,
                                 config_mod=cm, use_lowercase=use_lowercase)
        # apply patches
        # -- apply all patches from the __patches__ dicts
        for patch in globalsobj['SETTINGS_PATCHES_APPLIED']:
            patch_type = patch[0]
            patch_target = patch[1]
            patch_input = patch[2]
            patch_prepend = patch[3]
            patch_remove = patch[4]
            patch_at = patch[5]
            if patch_type == 'list':
                cls.patch_do_list(
                    globalsobj, patch_target, patch_input, patch_prepend,
                    patch_remove, patch_at)
            elif patch_type == 'dict':
                cls.patch_do_dict(
                    globalsobj, patch_target, patch_input, patch_remove)
            elif patch_type == 'func':
                cls.patch_do_func(globalsobj, patch_target, patch_input)
        # add api_keys from ./config/
        if cls.password:
            for ec in env_class:
                if globalsobj.get('API_KEYS_ENV'):
                    cls.apply_keys_from_env(globalsobj, ec)
                else:
                    cls.apply_keys_from_file(globalsobj, ec)
                if cls._allow_keys_patch:
                    for patch in globalsobj['SETTINGS_PATCHES_APPLIED']:
                        patch_type = patch[0]
                        patch_target = patch[1]
                        patch_input = patch[2]
                        if patch_type == 'keyspatch_func':
                            cls.patch_do_func(globalsobj,
                                              patch_target,
                                              patch_input, keyspatch=True)
        else:
            if globalsobj.get('API_KEYS', True):
                cls.info(
                    ("[WARN] KEYS are not loaded -- ENV_APIKEY_DECRYPT "
                     " is not set or empty"))

    @classmethod
    def info(cls, text):
        logger.info(text)
        if cls.verbose:
            print(text)

    @classmethod
    def warn(cls, text):
        logger.warn(text)
        if cls.verbose:
            print(text)

    @classmethod
    def error(cls, text):
        logger.error(text)
        if cls.verbose:
            print(text)

    @classmethod
    def fail(cls, text):
        # get the root logger and print the message as this fails with exit(1)
        print(text)

    @classmethod
    def apply_keys(cls, globalsobj, keys):
        """
        applies the key dictionary
        """
        cls._allow_keys_patch = keys.pop('ALLOW_KEYS_PATCH',
                                         cls._allow_keys_patch)
        if isinstance(cls._allow_keys_patch, string_types):
            cls._allow_keys_patch = cls._allow_keys_patch.split(',')
        if isinstance(keys, dict):
            globalsobj.update(keys)

    @classmethod
    def apply_keys_from_file(cls, globalsobj, ec):
        """
        read the keys from a key file, decrypt it and call apply_keys
        """
        if not 'API_KEYS_DIR' in globalsobj:
            return
        filename = globalsobj['API_KEYS_DIR'] + \
            ec + globalsobj['API_KEYS_FILE_EXTENSION']
        cls.info("[INFO] Loading keys for %s from %s" % (ec, filename))
        try:
            cipherfile = open(filename, 'r')
        except IOError:
            logging.error("Cannot load keys file: %s" % filename)
        else:
            try:
                cleartext = cls.aes.decrypt(cipherfile.read())
                keys = json.loads(cleartext)
            except Exception as e:
                msg = ("Could not decrypt keyfile %s. Did you set "
                       " ENV_APIKEY_DECRYPT correctly? %s" % (
                           filename, e))
                logging.error(msg)
                raise AssertionError(msg)
            else:
                cls.apply_keys(globalsobj, ec)

    @classmethod
    def apply_keys_from_env(cls, globalsobj, ec):
        """
        read the keys from an environment variable, decrypt it and call 
        apply_keys
        """
        keyname = '%s_KEYS' % ec
        cls.info("[INFO] Loading keys for %s from %s" % (ec, keyname))
        try:
            cleartext = cls.aes.decrypt(os.environ.get(keyname))
            keys = json.loads(cleartext)
        except Exception as e:
            msg = ("Could not read key %s from environment. Did you set"
                   " the key and ENV_APIKEY_DECRYPT correctly? %s" %
                   (keyname, e))
            logging.error(msg)
            raise AssertionError(msg)
        else:
            cls.apply_keys(globalsobj, keys)

    @classmethod
    def apply_config(cls, globalsobj, env_class=None, config_mod="config",
                     use_lowercase=False):
        """
        load env_class from module config_mod, and extract all
        settings parameters in the globals object.
        """
        mod = None
        if isinstance(env_class, string_types):
            try:
                logger.debug("Trying to load %s from %s" %
                             (env_class, config_mod))
                mod = import_module(config_mod)
                settings_cls = getattr(mod, env_class)
            except BaseException as e:
                cls.fail('[ERROR] Trying to load %s (%s), Exception was: %s' %
                         (env_class, mod, e))
                if '--traceback' in sys.argv:
                    from traceback import print_exc
                    print_exc()
                exit(1)
        else:
            settings_cls = env_class
        # loop through all base classes in reverse class lookup manner
        # (from top to bottom) so that overrides are possible
        logger.debug("Applying settings from %s.%s" % (config_mod, env_class))
        for base_cls in reversed(inspect.getmro(settings_cls)):
            if base_cls not in globalsobj['SETTINGS_APPLIED']:
                globalsobj['SETTINGS_APPLIED'].append(
                    "%s.%s" % (base_cls.__module__, base_cls.__name__))
                cls._config_modules.append(base_cls.__module__)
                for var in base_cls.__dict__:
                    if use_lowercase or isuppercase(var):
                        logger.debug("Setting %s from %s" % (var, base_cls))
                        globalsobj[var] = base_cls.__dict__[var]
                # register patches
                patches = base_cls.__dict__.get('__patches__', ())
                for patch in patches:
                    globalsobj['SETTINGS_PATCHES_APPLIED'].append(patch)
        dups = cls.check_duplicate_apps(globalsobj)
        if dups:
            print("[WARNING] Duplicates %s in INSTALLED_APPS" % dups)

    @classmethod
    def patches_from_applied_configs(cls, globalsobj):
        """
        return all patches from modules that have been applied. Patches
        from other modules were registered because the classes may be loaded
        independent of them being applied (e.g. if preloaded).
        """
        # if patches were applied previously they may
        # have been discarded from the module's patches
        # object, but still be present in the settings
        # => we always give precedence to those in the settings
        cls._patches = globalsobj.get('SETTINGS_PATCHES', cls._patches)
        globalsobj['SETTINGS_PATCHES'] = cls._patches
        applied_funcs = ([patch for patch in cls._patches
                          if patch.__module__ in cls._config_modules])
        globalsobj['SETTINGS_PATCHES_APPLIED_FUNC'] = applied_funcs
        return globalsobj['SETTINGS_PATCHES_APPLIED_FUNC']

    @classmethod
    def insert_patch(cls, patch):
        """
        attempts to insert patch into the configuration class

        To apply a patch, the configuration class must define the
        __patches__ class variable as a list of patches. This
        method attempts to find the configuration class' frame and
        insert __patches__ f_locals
        """
        try:
            for i in range(5):
                frame = sys._getframe(i).f_locals
                if frame.get('__module__') is not None:
                    break
        except ValueError:
            cls.warn('Cannot insert __patches__ for patch', patch)
        else:
            frame.setdefault('__patches__', [])
            frame['__patches__'].append(patch)

    @classmethod
    def patch(cls, func, *args):
        """
        record a patch function to be executed at end of all imports
        patches are executed in order of registration, which is
        equal to the reverse mro. A patch function receives the
        globals() object as its parameter
        """
        return cls.patch_func(func, args)

    @classmethod
    def patch_keys(cls, func, name, *args):
        """
        record a keys patch function to be executed after keys 
        have been applied. note that the given name must be
        registered in the decrypted keys, otherwise the patch will
        be refused 
        """
        args = list(args)
        args.insert(0, name)
        return cls.patch_keys_func(func, args)

    @classmethod
    def patch_middleware(cls, addl, prepend=False, remove=False, at=None):
        """
        convenience function to patch the middleware classes
        """
        addl = make_tuple(addl)
        return cls.patch_list('MIDDLEWARE_CLASSES', addl, prepend=prepend,
                              remove=remove, at=at)

    @classmethod
    def patch_apps(cls, addl, prepend=False, remove=False, at=None):
        """
        convenience function to patch the installed apps
        """
        addl = make_tuple(addl)
        return cls.patch_list('INSTALLED_APPS', addl, prepend=prepend,
                              remove=remove, at=at)

    @classmethod
    def patch_func(cls, func, args):
        patch = ('func', func, args, None, None, None)
        cls.insert_patch(patch)
        return patch

    @classmethod
    def patch_keys_func(cls, func, args):
        patch = ('keyspatch_func', func, args, None, None, None)
        cls.insert_patch(patch)
        return patch

    @classmethod
    def patch_list(cls, list_name, list_patch, prepend=False,
                   remove=False, at=None):
        patch = ('list', list_name, list_patch, prepend, remove, at)
        cls.insert_patch(patch)
        return patch

    @classmethod
    def patch_dict(cls, dict_name, dict_patch, remove=False):
        patch = ('dict', dict_name, dict_patch, False, remove, None)
        cls.insert_patch(patch)
        return patch

    @classmethod
    def report(cls, globalsobj, keys=None):
        keys = make_tuple(keys)
        print('-- SETTINGS as seen by EnvSettingsBase --\n')
        for k, v in iteritems(globalsobj):
            if not keys or k in keys:
                print("%s=%s\n" % (k, v))

    @classmethod
    def patch_do_func(cls, globalsobj, func, args, keyspatch=False):
        if keyspatch:
            # restrict to the given settings object
            # note this must be listed in keys' ALLOW_KEYS_PATCH
            _globalsobj = globalsobj
            globalsobj = {}
            globalsobj.update(_globalsobj)
            patch_element = args[0]
            assert patch_element in cls._allow_keys_patch, \
                "Keys patch is not allowed to access >%s<" % patch_element
        try:
            func(globalsobj, *args)
        except NameError:
            # backward compatiblity when we did not pass *args
            func(globalsobj)
        if keyspatch:
            # update settings as patched
            _globalsobj.update({patch_element: globalsobj.get(patch_element)})

    @classmethod
    def patch_do_list(cls, globalsobj, list_name, list_patch, prepend=False,
                      remove=False, at=None):
        """
        add a patch for list_name, applying list_patch. In case of remove,
        all items in list_patch will be removed from list_name
        """
        def prepend_or_append(globalsobj, list_name, list_patch):
            # helper function to prepend or append
            # list_patch to globalsobj

            # avoid duplicates
            patch_set = OrderedSet(list_patch)
            globals_set = OrderedSet(globalsobj[list_name])
            if not prepend:
                # "|" - this is a union operation
                globalsobj[list_name] = list(globals_set | patch_set)
            else:
                globalsobj[list_name] = list(patch_set | globals_set)

        if list_name not in globalsobj:
            globalsobj[list_name] = []
        if not remove:
            if not at:
                # prepend at head, or append to tail
                prepend_or_append(globalsobj, list_name, list_patch)
            else:
                # insert at specific position given by at parameter
                # which must be a value in the list
                list_topatch = list(globalsobj[list_name])
                try:
                    pos = list_topatch.index(at)
                except ValueError:
                    # if at value is not in list, revert to usual prepend
                    # or append
                    pos = len(list_topatch)
                    prepend_or_append(globalsobj, list_name, list_patch)
                else:
                    list_patch = list(list_patch)
                    list_patch.reverse()
                    for item in list_patch:
                        # avoid duplicates
                        if item not in globalsobj[list_name]:
                            list_topatch.insert(
                                pos if prepend else pos + 1, item)
                    if isinstance(globalsobj[list_name], tuple):
                        globalsobj[list_name] = tuple(list_topatch)
                    else:
                        globalsobj[list_name] = list_topatch

        else:
            # remove, i.e. new list contains all apps except those in
            # list_patch
            items = globalsobj[list_name]
            globalsobj[list_name] = tuple(
                [x for x in items if x not in list_patch])
        # warn if duplicates in apps
        if list_name == 'INSTALLED_APPS':
            # check for duplicates
            if cls.check_duplicate_apps(globalsobj):
                print ("WARNING: %s is duplicate in INSTALLED_APPS "
                       " (in patch_apps %s prepend=%s remove=%s at=%s)" %
                       (list_patch, prepend, remove))

    @classmethod
    def patch_do_dict(cls, globalsobj, dict_name, dict_patch, remove=False):
        """
        add a patch for dict_name, applying dict_patch. In case of
        remove the keys in dict_patch will be deleted from the dict
        referenced by dict_name
        """
        if dict_name not in globalsobj:
            globalsobj[dict_name] = {}
        if not remove:
            globalsobj[dict_name].update(dict_patch)
        else:
            # remove all keys in dict_name dictionary
            keys = globalsobj[dict_name].keys()
            diffs = set(dict_patch).difference(set(keys))
            for d in diffs:
                del globalsobj[dict_name][d]

    @classmethod
    def check_duplicate_apps(cls, globalsobj):
        if 'INSTALLED_APPS' in globalsobj:
            apps = globalsobj['INSTALLED_APPS']
            dups = set([app for app in apps if app.count(app) > 1])
            return dups
        return []


class StackableSettings(EnvSettingsBase):

    """
    This is the StackableSettings loader. Use as shown below. 

    Usage:
       manage.py:
           # put this before execute_from_command_line(), i.e.
           StackableSettings.parse_options()
           execute_from_command_line(sys.argv)

       settings.py:
           # refactor all your settings into the config module or package,
           # then your settings.py contains only these statements:
           from stackable import StackableSettings
           StackableSettings.load()

       wsgi.py:
           # you must run StackableSettings.parse_options() *before*
           # the import of get_wsgi_application. To do this safely,
           # the best practices is to remove the django.core.wsgi import
           # and replace it with the following code. This does the
           # same thing as before, but makes sure StackableSettings are
           # properly initialized.
           # from django.core.wsgi import get_wsgi_application() <<< remove!
           import os
           from shrutil.config_base import StackableSettings
           os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
           application = StackableSettings.get_wsgi_application()

        This will load the following configuration class from the 
        config module:

        1. as given by the --config option
        2. as set by the DJANGO_CONFIGURATION environment variable
        3. as set by the DJANGO_CONFIGURATION_TEST environment variable
           if 'manage.py test' is called

    To debug, call 

        manage.py --debug-config  print_settings | \
           grep -E "\[INFO|WARN|ERROR\]|ERROR|SETTINGS.*APPLIED"

    This will print all the configuration classes that were loaded, in 
    loading order, and all the patches that were applied, in the order applied.

    To load a specific configuration class from the command line, run e.g.

        manage.py --config Env_Developer

    This will load config.Env_Developer. You may specify the specific module
    to use by giving a full path, i.e. --config foo.Env_Developer  

    To print the effective settings after all configurations were applied,
    run the usual Django command:

        manage.py print_settings

    By default, API key decryption is automatically applied. To turn it
    off, override the default stackset.Config_ApiKey class like so:

    class Config_ApiKey(stacksettings.Config_ApiKey):
        API_KEYS = False

    If you need more control, use the setup() method, see
    EnvSettingsBase.setup() for details.
    """
    @classmethod
    def set_defaults(cls):
        os.environ.setdefault('DJANGO_CONFIGURATION', 'EnvSettings_Local')
        os.environ.setdefault(
            'DJANGO_CONFIGURATION_TEST', 'EnvSettings_LocalTest')

    @classmethod
    def parse_options(cls, argv=None):
        """
        StackableSettings.parse_options()
        """
        argv = argv or sys.argv
        if '--config' not in sys.argv:
            cls.set_defaults()
        else:
            index = sys.argv.index('--config')
            os.environ['DJANGO_CONFIGURATION'] = argv[index + 1]
            os.environ['DJANGO_CONFIGURATION_TEST'] = argv[index + 1]
            # delete both --config and value
            del argv[index]
            del argv[index]
        if '--debug-config' in sys.argv:
            index = sys.argv.index('--debug-config')
            EnvSettingsBase.verbose = True
            del argv[index]

    @classmethod
    def load(cls, globalsobj=None):
        """
        helper method to load from settings.py as simple as
        StackableSettings.load()
        """
        cls.set_defaults()
        if len(sys.argv) > 1 and sys.argv[1] == 'test':
            config = os.environ['DJANGO_CONFIGURATION_TEST']
        else:
            config = os.environ['DJANGO_CONFIGURATION']
        globalsobj = globalsobj or sys._getframe(1).f_globals
        EnvSettingsBase.setup(globalsobj, env_class=config)

    @classmethod
    def root_path(cls, filename=None):
        """
        this returns the parent directory of the top-level module of the
        configuration class, which is assumed to be in the actual root
        of the project 
        """
        if filename is None:
            filename = sys._getframe(1).f_globals.get('__file__')
        cur_dir = os.path.dirname(filename)
        return os.path.abspath(os.path.join(cur_dir, os.pardir))

    @classmethod
    def get_wsgi_application(cls):
        # parse_options must run *before* django's get_wsgi_appliction
        # in order to properly initialize StackableSettings
        StackableSettings.parse_options()
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()


class BadConfiguration(BaseException):
    pass


def make_tuple(input):
    """
    returns the input as a tuple. if a string is
    passed, returns (input, ). if a tupple is
    passed, returns the tupple unmodified
    """
    if not isinstance(input, (tuple, list)):
        input = (input,)
    return input


def isuppercase(name):
    return name == name.upper() and not name.startswith('_')
