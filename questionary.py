import inquirer

listFilter = [
    inquirer.Text('product', 'Qual produto deseja procurar?'),
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
        ignore=lambda x: x['typePayment'] != 'Crédito'),
    inquirer.List(
        'isShippingFree',
        message='É importante possuir frete grátis?',
        choices=['Sim', 'Não'],
        default='Sim'
    ),
]

dataForSearch = inquirer.prompt(listFilter)
