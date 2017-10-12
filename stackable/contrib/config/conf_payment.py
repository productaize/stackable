import os

from stackable.stackable import StackableSettings


def setup_payment_variants(settings, *args, **kwargs):
    """ override payment variants by patched keys """
    variants = settings.get('PAYMENT_VARIANTS')
    for processor, var in variants.values():
        # e.g. { 'default': ('processor', { ... }) }
        # => var is the dict
        for k, v in var.iteritems():
            # e.g. var = { 'client_id' : 'PAYPAL_CLIENT_ID' }
            # => v = PAYPAL_CLIENT_ID
            # => set { 'client-id' : settings.PAYPAL_CLIENT_ID }
            var[k] = settings.get(v) or var[k]
    settings['PAYMENT_VARIANTS'] = variants


class Config_DjangoPayments(object):

    """ config for django payments

    see https://django-payments.readthedocs.io/en/latest/install.html
    """
    _apps_ = (
        'payments',
        'orders',
    )

    StackableSettings.patch_apps(_apps_)
    StackableSettings.patch_keys(setup_payment_variants, 'PAYMENT_VARIANTS')

    PAYMENT_HOST = os.environ.get('PAYMENT_HOST', 'localhost:8000')
    PAYMENT_USES_SSL = True
    PAYMENT_MODEL = 'landingpage.orders.Payment'

    PAYPAL_CLIENT_ID = ''
    PAYPAL_SECRET = ''
    PAYPAL_ENDPOINT = 'https://api.sandbox.paypal.com'

    PAYMENT_VARIANTS = {
        #'default': ('payments.dummy.DummyProvider', {}),
        'default': ('payments.paypal.PaypalProvider', {
            # actual values are patched from keys in setup_payment_variants
            'client_id': 'PAYPAL_CLIENT_ID',
            'secret': 'PAYPAL_SECRET',
            'endpoint': 'PAYPAL_ENDPOINT',
            'capture': True})
    }
