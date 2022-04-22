from moltin_api import get_actual_token
from moltin_api import get_product_img_url
from moltin_api import get_stock_data


def fetch_caption(product_data):
    moltin_token = get_actual_token()

    name = product_data['name']
    description = product_data['description']
    price_usd = product_data[
        'meta']['display_price']['with_tax']['formatted']
    price_amount = product_data[
        'meta']['display_price']['with_tax']['amount']
    price_for_10kg = format(int(price_amount) / 100 * 10, '.2f')
    available = get_stock_data(moltin_token, product_data['id'])['available']

    caption = f'{name}'
    caption += f'\n\n{price_usd} per kg'
    caption += f'\n{available} kg on stock'
    caption += f'\n\n{description}'
    caption += f'\n\n10 kg in cart for ${price_for_10kg}'

    return caption


def fetch_img_url(product_data):
    img_data = product_data['relationships'].get('main_image')['data']

    if img_data:
        img_id = img_data['id']

    else:
        return

    if img_id:
        moltin_token = get_actual_token()

        return get_product_img_url(moltin_token, img_id)


def fetch_cart_description(cart_items_data):
    text = ''

    for item in cart_items_data['data']:
        if text != '':
            text += '\n\n'

        product_name = item['name']
        price_formatted = item['meta']['display_price']['with_tax']['unit'][
            'formatted']
        price_integer = int(
            item['meta']['display_price']['with_tax']['unit']['amount']) / 100
        quantity = item['quantity']
        position_price = format(int(quantity) * price_integer, '.2f')

        text += f'<b>{product_name}</b>'
        text += f'\n{price_formatted} per kg'
        text += f'\n{quantity} kg in the cart for ${position_price}'

    cart_price = cart_items_data['meta']['display_price']['with_tax'][
        'formatted']

    text += f'\n\n\n<b>Total: {cart_price}</b>'
    return text
