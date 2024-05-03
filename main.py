import os
import sys

import qrcode
import requests
from dotenv import load_dotenv

class Shortener:
    @staticmethod
    def get_api_url():
        return os.getenv('API_URL')

    @staticmethod
    def get_headers():
        return {
            'x-api-key': os.getenv('API_KEY'),
            'Content-Type': 'application/json',
        }

    @classmethod
    def put_data(cls, table_name, item):
        data = {
            "TableName": table_name,
            "Item": item,
        }
        response = requests.post(
            cls.get_api_url(),
            json=data,
            headers=cls.get_headers())
        response.raise_for_status()
        # print(response.json())

    @classmethod
    def get_data(cls, table_name, key_name, key_value):
        params = {
            "table_name": table_name,
            "key_name": key_name,
            "key_value": key_value,
        }
        response = requests.get(
            cls.get_api_url(),
            params=params,
            headers=cls.get_headers())
        response.raise_for_status()
        return response.json()

    @classmethod
    def create_url(cls, origin, shorten):
        if cls.get_data('URL_TO_S8L', 'origin', origin):
            return 'Origin already exists'
        if cls.get_data('S8L_TO_URL', 'shorten', shorten):
            return 'Shorten already exists'
        item = {
            'origin': {'S': origin},
            'shorten': {'S': shorten},
        }
        cls.put_data('S8L_TO_URL', item)
        cls.put_data('URL_TO_S8L', item)
        img = qrcode.make(f'{os.getenv("BASE_URL")}/{shorten}')
        img.save(f'{shorten}.png')
        return 'Success'

if __name__ == '__main__':
    load_dotenv()
    # shell command에서 전달 받기
    print(Shortener.create_url(sys.argv[1], sys.argv[2]))