import os
import re

import requests
from dotenv import load_dotenv
from transliterate import translit

load_dotenv()


class StripeService:
    main_url = 'https://api.stripe.com/v1/'
    headers = {'Authorization': f'Bearer {os.getenv("STRIPE_APIKEY")}'}

    @classmethod
    def create_product(cls, product_id, name, description):
        response = requests.post(url=f'{cls.main_url}products',
                                 data={'id': convert_to_valid_format(f'{name}_{product_id}'), 'name': name,
                                       'description': description},
                                 headers=cls.headers)
        return response.json()

    @classmethod
    def create_price(cls, price, product_id, name):
        response = requests.post(url=f'{cls.main_url}prices',
                                 data={"unit_amount": price, "currency": "usd", "recurring[interval]": "month",
                                       "product": convert_to_valid_format(f'{name}_{product_id}')},
                                 headers=cls.headers)
        return response.json()

    @classmethod
    def create_billing_url(cls, product_id, name, bayer_id):
        price = requests.get(
            url=f'{cls.main_url}prices?product={convert_to_valid_format(name + "_" + str(product_id))}',
            headers=cls.headers).json().get("data")[0]["id"]
        response = requests.post(url=f'{cls.main_url}checkout/sessions',
                                 data={"line_items[0][price]": price, "line_items[0][quantity]": 1,
                                       "mode": "subscription",
                                       "success_url": f"http://127.0.0.1:8000/edu/subscribes/activate?user={bayer_id}&course={product_id}"},
                                 headers=cls.headers)
        return response.json().get('url')


def convert_to_valid_format(input_string):
    transliterated_string = translit(input_string, 'ru', reversed=True)
    valid_string = re.sub(r'[^a-zA-Z0-9_\-]', '_', transliterated_string)
    valid_string = re.sub(r'[_\-]+', '_', valid_string)
    valid_string = valid_string.strip('_')
    return valid_string
