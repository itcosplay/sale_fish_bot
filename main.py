import logging
import requests
import pprint

from environs import Env


logger = logging.getLogger(__file__)


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    env = Env()
    env.read_env()

    token = env('ACCESS_TOKEN')

    # headers = {
    #     'Authorization': f'Bearer {token}',
    # }

    data = {
        'client_id': 'ctazZvYvkivqq0SBiKLnoxrvPHQfqE7uTEz1wVafYW',
        'grant_type': 'implicit',
    }

    # response = requests.get('https://api.moltin.com/v2/products', headers=headers)
    response = requests.post('https://api.moltin.com/oauth/access_token', data=data)
    response.raise_for_status()

    pprint.pprint(response.text)


if __name__ == '__main__':
    main()
