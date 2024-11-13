import json
import os
import sys
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from unidecode import unidecode

currentDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.dirname(currentDir)

sys.path.append(rootDir)

from questionary import dataForSearch


def product_name_fix(productName):
    productNameLower = productName.lower()
    productNameNormalize = unidecode(productNameLower)
    return '-'.join(productNameNormalize.split())


def validate_product_find(productListed):
    if (
        productFormatted in productListed['friendlyName']
        and bool(productListed['available'])
        and productListed['sellerName'] == 'KaBuM!'
    ):
        return True

    return False


def format_to_real(value):
    real, cents = format(value, ',.2f').split('.')
    return f'R$ {real.replace(',', '.')},{cents}'

productFormatted = product_name_fix(dataForSearch['product'])

url = f'https://www.kabum.com.br/busca/{productFormatted}?page_number=1&page_size=100&sort=price'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'}

try:
    response = requests.get(url, headers=headers)

    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    recoveryProducts = json.loads(soup.find('script', attrs={'id': '__NEXT_DATA__'}).text)

    products = recoveryProducts['props']['pageProps']['data']['catalogServer']['data']

    resultFinal = []

    for product in products:
        if validate_product_find(product):
            print(json.dumps(product, indent=4))

            productObject = {}

            if not product['code'] is None:
                productObject['cd_product'] = int(product['code'])
                productObject['ds_product_link'] = f'https://www.kabum.com.br/produto/{product['code']}'

            if not product['name'] is None:
                productObject['nm_product'] = product['name']

            if not product['manufacturer'] is None:
                if not product['manufacturer']['name'] is None:
                    productObject['nm_brand'] = product['manufacturer']['name']

            if not product['thumbnail'] is None:
                productObject['ds_img_link'] = product['thumbnail']

            if not product['category'] is None:
                productObject['ds_category'] = product['category']

            if not product['warranty'] is None:
                productObject['ds_warranty'] = product['warranty']

            if not product['rating'] is None:
                productObject['nr_rating'] = int(product['rating'])

            if not product['ratingCount'] is None:
                productObject['qt_rating'] = int(product['ratingCount'])

            if not product['offer'] is None:
                if not product['offer']['quantityAvailable'] is None:
                    productObject['qt_product'] = int(product['offer']['quantityAvailable'])

                if not product['offer']['name'] is None:
                    productObject['nm_offer'] = product['offer']['name']

                if not product['offer']['startsAt'] is None:
                    productObject['dt_offer_start'] = f'{datetime.fromtimestamp(product['offer']['startsAt'], tz = None)}'

                if not product['offer']['endsAt'] is None:
                    productObject['dt_offer_end'] = f'{datetime.fromtimestamp(product['offer']['endsAt'], tz = None)}'

            if not product['price'] is None:
                productObject['qt_price'] = format_to_real(product['price'])

            if not product['priceWithDiscount'] is None:
                productObject['qt_price_discounted'] = format_to_real(product['priceWithDiscount'])

            if not product['discountPercentage'] is None:
                productObject['qt_discount_percentage'] = f'{product['discountPercentage']}%'

            if not product['ufsFlash'] is None:
                productObject['st_uf_flash_delivery'] = product['ufsFlash']

            if not product['flags'] is None:
                if not product['flags']['isMarketplace'] is None:
                    productObject['is_marketplace'] = product['flags']['isMarketplace']

                if not product['flags']['isOpenbox'] is None:
                    productObject['is_openbox'] = product['flags']['isOpenbox']

                if not product['flags']['isFreeShipping'] is None:
                    productObject['is_free_shipping'] = product['flags']['isFreeShipping']

                if not product['flags']['isPrime'] is None:
                    productObject['is_prime'] = product['flags']['isPrime']

                if not product['flags']['isFreeShippingPrime'] is None:
                    productObject['is_free_shipping_prime'] = product['flags']['isFreeShippingPrime']

            resultFinal.append(productObject)
except requests.exceptions.HTTPError as err:
    print(f'HTTP error occurred: {err}')
except Exception as e:
    print(f'Error occurred while parsing HTML: {e}')