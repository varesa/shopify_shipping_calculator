import shopify

def get_api_key():
    apikey = ""
    with open("auth_apikey", 'r', encoding="utf-8") as file_apikey:
        apikey = file_apikey.readline()
    return apikey

def get_password():
    password = ""
    with open("auth_password", 'r', encoding="utf-8") as file_password:
        password = file_password.readline()
    return password

def create_session():
    shop_url = "https://%s:%s@SHOP_NAME.myshopify.com/admin" % (get_api_key(), get_password())
    shopify.ShopifyResource.set_site(shop_url)