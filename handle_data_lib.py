from moltin_api import get_product_img_url

def create_product_description_text(product_data):
    product_name = product_data['name']
    product_description = product_data['description']
    product_price = product_data[
        'meta']['display_price']['with_tax']['formatted']
    
    img_data = product_data['relationships'].get('main_image')['data']

    if img_data:
        product_img_id = img_data['id']

    else:
        product_img_id = None

    # if product_img_id:
    #     product_img_url = get_product_img_url(token, product_img_id)

    return 'Here will be prod descr...'