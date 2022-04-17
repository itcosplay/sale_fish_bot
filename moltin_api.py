import requests
import pprint

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

    return response.json()


def check_token(token, client_id, client_secret):
    if token['expires'] <= datetime.timestamp(datetime.now()):

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

