#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


import shopify

from .config_manager import config_shopapikey, config_shoppassword, config_shopname


def create_session():
    """
    Authenticate shopify_python_api with tokens from the config
    :return: -
    """
    shop_url = "https://%s:%s@%s.myshopify.com/admin" % (config_shopapikey(), config_shoppassword(), config_shopname())
    shopify.ShopifyResource.set_site(shop_url)