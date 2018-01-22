Stackable Configuration
=======================

Stackable is a drop-in replacement for Django's settings `settings.py` that is ideally suited for 12factor apps:

* environment-specific configuration settings
* modular configuration settings
* object oriented with subclassing
* configuration settings are stackable 
* secret data handling (keys, passwords)

Using this approache gives us several benefits from the traditional Django `settings`, 
in particular the complexity becomes manageable.

How it works
------------

StackableSettings uses Python standard classes and multi-inheritance to compose settings. Example:

```
# config.py
EnvSettings_GLOBAL(object):
  # standard apps
  INSTALLED_APPS=(
     ...
  )
  SOME_SETTING='foo'
  
Config_SomeApp(object):
  APP_CONFIG='baz'

EnvSettings_Local(EnvSettings_GLOBAL):
  # additional settings for local testing
  SOME_SETTING='bar'
  APP_CONFIG='testing'

# load order is in reverse, that is first EnvSettings_GLOBAL,
# then Config_SomeApp. In other words, Config_SomeApp overrides
# any variable set by EnvSettings_GLOBAL.
EnvSettings_production(Config_SomeApp,
                      EnvSettings_GLOBAL):
  SOME_SETTING='prod'
  
# settings.py
StackableSettings.load()
```   
   
Running manage.py will load config.py (or a config module) and import the
settings classes. Settings are loaded by loading a class and all its
superclasses, applying all capitalized variables from the class to the 
settings.py's local() scope, which is the same as having capitalized variables 
in settings.py directly. Note that only CAPITALIZED variables are loaded. 

The settings class to load is given by the DJANGO_CONFIGURATION env variable, 
and it defaults to EnvSettings_Local. You can find it in the 
app's ./config module. In ./deploy/common there are several configuration 
classes that can be used across deployable apps.

In the above example, SOME_SETTING will have the value 'bar' if DJANGO_CONFIGURATION
is either not set or has the value 'EnvSettings_local'. It will have the value
'prod' if DJANGO_CONFIGURATION was set to 'EnvSettings_production'.


Patches
=======

The way we load settings is by going through the list of classes in the class 
specified in $DJANGO_CONFIGURATION. So you have EnvSettings_collect that 
has a bunch of classes listet in it. What the settings loader does is take all
the UPPER_CASE_VARIABLES and add it each to list of settings, whereby existing
settings are overwritten by those loaded later. So if you have 

```
class SomeEnv(object):
 FOO_BAZ = ('xyz',)
 
class MyEnv(SomeEnv)
 FOO_BAZ = ('abc',)

```
     
and load MyEnv, you'll end up with FOO_BAZ==tuple('abc'). Something like 
FOO_BAZ += 'abc' won't work as it would simply replace what was there before. 

That's why we need to use a *patch*:

```
class MyEnv(SomeOther)
  _addtl_foo_baz = ('abc',)
  __patches__ = StackableSettings.patch(
      StackableSettings.patch_list('FOO_BAZ', _addtl_foo_baz),
  )
```

Which results in FOO_BAZ == tuple('xyz', 'abc'). There are several patch methods,
see StackableSettings.


Secret Key Handling
===================

In order to not expose production keys to everyone on the team, StackableSettings 
implements a simple keychain using environment variables or files. With this approach, 
the settings classes only contain place holder values, which get replaced 
at run-time by the real keys and secrets. The keys to be applied are retrieved 
according to the `DJANGO_CONFIGURATION` env variable so that each environment can
use different keys.
 
Keys are either stored in an encrypted environment variable or an encrypted file. 
A source file by default lives in `~/.stackable/keys.yml` and is organized by
environment name. They `keys.yml` file looks something like this:

```
# yml
EnvSettings_Local:
   SOME_SETTING: SECRET
   
EnvSettings_Production:
   SOME_SETTING: OTHER_SECRET
...
```

To create the encrypted environment variable:

```
$ python -m stackable.encryptkeys
Creating variables for stackable from /home/patrick/.stackable/keys.yml
Set the environment for stackable as follows:
---
export DJANGO_CONFIGURATION=EnvSettings_Local DJANGO_CONFIGURATION_TEST=EnvSettings_Local ENV_APIKEY_DECRYPT=ce77e82d-b0a2-4007-9380-d7fddd4bd420 EnvSettings_Local_KEYS=VydQzauHmTnqladba+oU16w=
```

To enable encrypted keys in your EnvSettings class:

```
from stackable.contrib.conf_api import Config_ApiKeys

class EnvSettings_XYZ(Config_ApiKeys, 
                      ...):
    pass
```

`Config_ApiKeys` triggers stackable to read encrypted keys from the environment. 
See its definition for more details on available options.  

TODO
* implement a Django command for this

