from ecommerces.kabum import find_product
from helpers.handle import product_name_fix
from helpers.questionary import dataForSearch

product = product_name_fix(dataForSearch['product'])

find_product(product)
