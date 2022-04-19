import os
import requests

from datetime import datetime
from environs import Env


def get_access_token(client_id, client_secret):
    url = 'https://api.moltin.com/oauth/access_token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }

    response = requests.post(url, data=data)
    response.raise_for_status()

    token_data = response.json()

    os.environ.setdefault('MOLTIN_TOKEN', token_data['access_token'])
    os.environ.setdefault('MOLTIN_TOKEN_EXPIRES', str(token_data['expires']))

    return token_data['access_token']


def get_actual_token():
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    try:
        if os.environ['MOLTIN_TOKEN']:
            token = os.environ['MOLTIN_TOKEN']

    except KeyError:
        return get_access_token(client_id, client_secret)

    token_expires = os.environ['MOLTIN_TOKEN_EXPIRES']

    if float(token_expires) <= datetime.timestamp(datetime.now()):

        return get_access_token(client_id, client_secret)

    else:

        return token


def get_products(access_token):
    url = 'https://api.moltin.com/v2/products'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['data']


def get_product(access_token, product_id):
    url = f'https://api.moltin.com/v2/products/{product_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_product_img_url(access_token, img_id):
    url = f'https://api.moltin.com/v2/files/{img_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()['data']['link']['href']


def get_or_create_cart(access_token, cart_id, currency='USD'):
    url = f'https://api.moltin.com/v2/carts/{cart_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-MOLTIN-CURRENCY': currency
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def add_to_cart(
    access_token,
    cart_id,
    item_id,
    item_quantity,
    currency='USD'
):
    url = f'https://api.moltin.com/v2/carts/{cart_id}/items'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-MOLTIN-CURRENCY': currency
    }

    cart_item = {
        'data': {
            'id': item_id,
            'type': 'cart_item',
            'quantity': item_quantity,
        }
    }

    response = requests.post(url, headers=headers, json=cart_item)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    env = Env()
    env.read_env()

    client_id = env.str('CLIENT_ID')
    client_secret = env.str('CLIENT_SECRET')

    access_token = get_access_token(client_id, client_secret)
    print(access_token)
    # access_token = '0388c8fc1485a163ad70fe0a08d4bd4bf1104ce8'


    products = get_products(access_token)
    
    # for product in products:
    #     pprint.pprint(product)
    #     print('=====')

    # {'token_type': 'Bearer', 'expires_in': 3600, 'access_token': 'd4ef00ccd24082baa05b1932c10be8d5142da0ae', 'expires': 1650186737, 'identifier': 'client_credentials'}

