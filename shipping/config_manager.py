import sys
from os.path import join, exists

import yaml

basepath = join("shipping", "config")

path_shopify = join(basepath, "shopify.yaml")

default_shopify = """
shop_name:
shop_apikey:
shop_passwd:
"""

def initialize_configs():
    if not exists(path_shopify):
        with open(path_shopify, 'w') as file_shopify:
            file_shopify.write(default_shopify)

        print('Config file for shopify missing')
        print('Default file created, please edit in values')
        sys.exit(1)

def config_shopname():
    with open(path_shopify, 'r') as file_shopify:
        config = yaml.safe_load(file_shopify)
        return config['shop_name']

def config_shopapikey():
    with open(path_shopify, 'r') as file_shopify:
        config = yaml.safe_load(file_shopify)
        return config['shop_apikey']

def config_shoppassword():
    with open(path_shopify, 'r') as file_shopify:
        config = yaml.safe_load(file_shopify)
        return config['shop_passwd']
