import shopify
import os.path

path = os.path.join("shipping", "config")

def get_api_key():
    apikey = ""
    with open(os.path.join(path, "auth_apikey"), 'r', encoding="utf-8") as file_apikey:
        apikey = file_apikey.readline()
    return apikey

def get_password():
    password = ""
    with open(os.path.join(path, "auth_password"), 'r', encoding="utf-8") as file_password:
        password = file_password.readline()
    return password

def get_shopname():
    shopname = ""
    with open(os.path.join(path, "shopname"), 'r', encoding="utf-8") as file_shopname:
        shopname = file_shopname.readline()
    return shopname

def create_session():
    shop_url = "https://%s:%s@%s.myshopify.com/admin" % (get_api_key(), get_password(), get_shopname())
    shopify.ShopifyResource.set_site(shop_url)