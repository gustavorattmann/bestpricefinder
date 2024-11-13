import json
import os
import requests
import sys
from unidecode import unidecode
from bs4 import BeautifulSoup

currentDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.dirname(currentDir)

sys.path.append(rootDir)

from questionary import dataForSearch


def product_name_fix(productName):
    productNameLower = productName.lower()
    productNameNormalize = unidecode(productNameLower)
    return '-'.join(productNameNormalize.split())


def validate_product_find(product):
    if productFormatted in product['friendlyName']:
        return True
    # elif dataForSearch['productBrand'] and dataForSearch['productBrand'] in product['manufacturer']['name']:
    #    return True
    else:
        return False


productFormatted = product_name_fix(dataForSearch['product'])

url = f'https://www.kabum.com.br/busca/{productFormatted}?page_number=1&page_size=100&sort=price'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'}

try:
    response = requests.get(url, headers=headers)

    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    recoveryProducts = json.loads(soup.find('script', attrs={'id': '__NEXT_DATA__'}).text)

    products = recoveryProducts['props']['pageProps']['data']['catalogServer']['data']

    for product in products:
        if validate_product_find(product):
            code = product['code']
            print(f'Código: {code}\n')
            name = product['name']
            print(f'Nome: {name}\n')
except requests.exceptions.HTTPError as err:
    print(f'HTTP error occurred: {err}')
except Exception as e:
    print(f'Error occurred while parsing HTML: {e}')
