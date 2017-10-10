from stackable.stackable import StackableSettings


class Config_DjangoCMSCascade(object):

    """
    django cms cascade setup
    configuration for Django CMS 3.2.5 with Django 1.7
    """
    # http://djangocms-cascade.readthedocs.org/en/latest/installation.html
    # there are several core issues with this
    # -- doesn't install the static files (missing in MANIFEST)
    # -- doesn't properly register models with reversion
    # -- in general doesn't seem to actually work -- nice try
    # see https://github.com/jrief/djangocms-cascade/issues
    # this comment is related to @0.4.5
    _apps_ = (
        'cmsplugin_cascade',
        'cmsplugin_cascade.extra_fields',  # optional
        'cmsplugin_cascade.sharable',      # optional
        'cmsplugin_cascade.generic',      # optional
        # 'cmsplugin_cascade.segmentation',  # optional -- fails in 3.2.5
    )
    _cascade_plugin_ = {
        # other settings
        # http://djangocms-cascade.readthedocs.io/en/latest/generic-plugins.html
        'plugins_with_extra_render_templates': {
            'CustomSnippetPlugin': [
                ('cms/cascade.html',
                 "Custom Template Identifier"),
                # other tuples
            ],
        },
        # add plugins that can go into e.g. a row. these are so called
        # leaf plugins
        'alien_plugins': ('TextPlugin', 'FilerImagePlugin',
                          'UserSignupPlugin',),
        # allow inline css custom classes and ids
        # this is great to limit what users can do. it's a mess if you love
        # freedom. I love freedom. -- miraculixx
        # http://djangocms-cascade.readthedocs.io/en/latest/customize-styles.html#configure-a-cascade-plugins-to-accept-extra-fields
        #'plugins_with_extra_fields': (
        #    'BootstrapButtonPlugin', 'BootstrapRowPlugin',
        #    'SimpleWrapperPlugin', 'HorizontalRulePlugin',
        #),
    }

    CMSPLUGIN_CASCADE_PLUGINS = ('cmsplugin_cascade.bootstrap3',)
    CMSPLUGIN_CASCADE_PLUGINS += ('cmsplugin_cascade.link',)
    CMSPLUGIN_CASCADE_PLUGINS += ('cmsplugin_cascade.generic',)
    CMSPLUGIN_CASCADE_PLUGINS += ('cmsplugin_cascade.segmentation',)
    __patches__ = (
        StackableSettings.patch_apps(_apps_, prepend=True, at='cms'),
        StackableSettings.patch_dict('CMSPLUGIN_CASCADE', _cascade_plugin_)
    )
