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


def format_date_to_brazil(date):
    convertDateToUtc = datetime.fromtimestamp(date, tz=None)
    dateFormatted = convertDateToUtc.strftime('%d/%m/%Y %H:%M:%S')
    return dateFormatted


def handle_object(dataOfObject):
    objectPreparation = {}

    if not dataOfObject['code'] is None:
        objectPreparation['cd_product'] = int(dataOfObject['code'])
        objectPreparation['ds_product_link'] = f'https://www.kabum.com.br/produto/{product['code']}'

    if not dataOfObject['name'] is None:
        objectPreparation['nm_product'] = dataOfObject['name']

    if not dataOfObject['manufacturer'] is None:
        if not dataOfObject['manufacturer']['name'] is None:
            objectPreparation['nm_brand'] = dataOfObject['manufacturer']['name']

    if not dataOfObject['thumbnail'] is None:
        objectPreparation['ds_img_link'] = dataOfObject['thumbnail']

    if not dataOfObject['category'] is None:
        objectPreparation['ds_category'] = dataOfObject['category']

    if not dataOfObject['warranty'] is None:
        objectPreparation['ds_warranty'] = dataOfObject['warranty']

    if not dataOfObject['rating'] is None:
        objectPreparation['nr_rating'] = int(dataOfObject['rating'])

    if not dataOfObject['ratingCount'] is None:
        objectPreparation['qt_rating'] = int(dataOfObject['ratingCount'])

    if not dataOfObject['offer'] is None:
        if not dataOfObject['offer']['quantityAvailable'] is None:
            objectPreparation['qt_product'] = int(dataOfObject['offer']['quantityAvailable'])

        if not dataOfObject['offer']['name'] is None:
            objectPreparation['nm_offer'] = dataOfObject['offer']['name']

        if not dataOfObject['offer']['startsAt'] is None:
            objectPreparation['dt_offer_start'] = format_date_to_brazil(dataOfObject['offer']['startsAt'])

        if not dataOfObject['offer']['endsAt'] is None:
            objectPreparation['dt_offer_end'] = format_date_to_brazil(dataOfObject['offer']['endsAt'])

    if not dataOfObject['price'] is None:
        objectPreparation['qt_price'] = format_to_real(dataOfObject['price'])

    if not dataOfObject['priceWithDiscount'] is None:
        objectPreparation['qt_price_discounted'] = format_to_real(dataOfObject['priceWithDiscount'])

    if not dataOfObject['discountPercentage'] is None:
        objectPreparation['qt_discount_percentage'] = f'{dataOfObject['discountPercentage']}%'

    if not dataOfObject['ufsFlash'] is None:
        objectPreparation['st_uf_flash_delivery'] = dataOfObject['ufsFlash']

    if not dataOfObject['flags'] is None:
        if not dataOfObject['flags']['isMarketplace'] is None:
            objectPreparation['is_marketplace'] = dataOfObject['flags']['isMarketplace']

        if not dataOfObject['flags']['isOpenbox'] is None:
            objectPreparation['is_openbox'] = dataOfObject['flags']['isOpenbox']

        if not dataOfObject['flags']['isFreeShipping'] is None:
            objectPreparation['is_free_shipping'] = dataOfObject['flags']['isFreeShipping']

        if not dataOfObject['flags']['isPrime'] is None:
            objectPreparation['is_prime'] = dataOfObject['flags']['isPrime']

        if not dataOfObject['flags']['isFreeShippingPrime'] is None:
            objectPreparation['is_free_shipping_prime'] = dataOfObject['flags']['isFreeShippingPrime']

    return objectPreparation


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
            productObject = handle_object(product)

            if productObject:
                resultFinal.append(productObject)

                print(json.dumps(resultFinal, ensure_ascii=False, indent=4))
            else:
                print('Nenhum resultado encontrado!')
except requests.exceptions.HTTPError as err:
    print(f'HTTP error occurred: {err}')
except Exception as e:
    print(f'Error occurred while parsing HTML: {e}')