#!/usr/bin/env python3

import requests


TELE_API_URL = 'https://api.telegram.org/bot{}/{}'


def read_token(token_path):
    with open(token_path) as f:
        return f.readline().strip()


def simple_method(token, method='getMe'):
    print(TELE_API_URL.format(token, method))
    responce = requests.get(TELE_API_URL.format(token, method))
    return responce.json()


if __name__ == '__main__':
    print(simple_method(read_token('tele_token')))
