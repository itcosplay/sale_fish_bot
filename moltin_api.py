import os
from pprint import pprint
import requests

from datetime import datetime
from environs import Env
from pprint import pprint

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

def get_stock_data(access_token, product_id):
    url = f'https://api.moltin.com/v2/inventories/{product_id}'
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
    pprint(response.json())
    return response.json()['data']


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


def add_to_cart(access_token, cart_id, item_id, item_quantity,
                currency='USD'):
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


def get_cart_items(access_token, cart_id):
    url = f'https://api.moltin.com/v2/carts/{cart_id}/items'

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def create_customer(access_token, email, name=None):
    url = 'https://api.moltin.com/v2/customers'

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    customer = {
        'data': {
            'type': 'customer',
            'name': name if name else email,
            'email': email,
        },
    }

    response = requests.post(url, headers=headers, json=customer)
    response.raise_for_status()

    return response.json()


def get_customer(access_token, customer_id):
    url = f'https://api.moltin.com/v2/customers/{customer_id}'

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def add_customer_to_cart(access_token, cart_id, customer_id):
    url = f'https://api.moltin.com/v2/carts/{cart_id}/relationships/customers'

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    customer = {
        'data': [
            {
                'type': 'customer',
                'id': customer_id,
            },
        ],
    }

    response = requests.post(url, headers=headers, json=customer)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    env = Env()
    env.read_env()

    # data = get_access_token(
    #     'ctazZvYvkivqq0SBiKLnoxrvPHQfqE7uTEz1wVafYW',
    #     '8ZiMoV9j6iXnnTZvtxZNKpXRPCO10LiYZoQQ1A0pNG')

    token = ''

    data = get_or_create_cart(token, 59677456)

    # data = add_to_cart(token,
    #                    59677456, 'f6123dbb-3f8a-430d-a962-000f7258f321', 1)

    # data = get_cart_items(token, 59677456)

    # data = create_customer(token, 'abs@mail.ru', 'KOSPLAY')

    # data = get_customer(token, '345e4775-567c-4f1b-9d0b-67019146f9b1')

    # data = add_customer_to_cart(
    #     token, 59677456, '345e4775-567c-4f1b-9d0b-67019146f9b1')

    pprint(data)
    

    #####    

    #  'relationships': {'items': {'data': None}},

    # 'relationships': {'customers': {},
    #                   'items': {'data': [{'id': 'fbe168c5-690c-4528-b9f1-d7431b4a8a4c',
    #                                             'type': 'cart_item'}]}},