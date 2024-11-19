import os
import sys

sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from helpers.handle import *

import json
import requests
from bs4 import BeautifulSoup


def find_product(findedProduct):
    url = f'https://www.kabum.com.br/busca/{findedProduct}?page_number=1&page_size=100&sort=price'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'}

    try:
        response = requests.get(url, headers=headers)

        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        recoveryProducts = json.loads(soup.find('script', attrs={'id': '__NEXT_DATA__'}).text)

        products = recoveryProducts['props']['pageProps']['data']['catalogServer']['data']

        resultFinal = []

        for product in products:
            if validate_product_find(findedProduct, product):
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
