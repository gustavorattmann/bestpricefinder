import brazilcep
import inquirer
from inquirer.errors import ValidationError
from inquirer.themes import BlueComposure


def validate_product(answer, current):
    if not current:
        raise ValidationError('', reason='É obrigatório informar o produto desejado!')

    return True


def validate_installment(answer, current):
    if not current:
        raise ValidationError('', reason='É obrigatório informar a quantidade de parcela(s)!')
    elif not current.isnumeric():
        raise ValidationError('', reason='Inserir apenas número(s)!')
    elif not int(current) > 1 or not int(current) < 13:
        raise ValidationError('', reason='Informar a quantidade de parcelas entre 1 e 12!')

    return True


def validate_cep(answer, current):
    if not current:
        raise ValidationError('', reason='É obrigatório informar um CEP!')
    else:
        address = brazilcep.get_address_from_cep(current)

        if not address:
            raise ValidationError('', reason='Informe um CEP válido!')

    return True


listFilter = [
    inquirer.Text('product', 'Qual produto deseja procurar?', validate=validate_product),
    inquirer.Text('productBrand', 'Qual a marca do produto deseja procurar?'),
    inquirer.Text('maxPrice', 'Qual o valor máximo aceitável (R$)?'),
    inquirer.List(
        'typePayment',
        message='Qual a forma de pagamento?',
        choices=['Dinheiro', 'Pix', 'Paypal', 'Crédito', 'Débito'],
        default='Pix'
    ),
    inquirer.Text(
        'installment',
        message='Deseja parcelar em até quantas vezes (Entre 1 e 12)?',
        ignore=lambda x: x['typePayment'] != 'Crédito',
        validate=validate_installment
    ),
    inquirer.List(
        'isPostalCode',
        message='Deseja verificar os fretes disponíveis para o seu endereço?',
        choices=['Sim', 'Não'],
        default='Sim'
    ),
    inquirer.Text(
        'zipCode',
        'Informe seu CEP para verificarmos os fretes',
        ignore=lambda x: x['isPostalCode'] == 'Não',
        validate=validate_cep
    ),
    inquirer.List(
        'isShippingFree',
        message='É importante possuir frete grátis?',
        choices=['Sim', 'Não'],
        default='Sim'
    ),
]

dataForSearch = inquirer.prompt(listFilter, theme=BlueComposure())
