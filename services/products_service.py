from flask import Flask
from commons.utils import products
from commons.utils import read_json

app = Flask(__name__)


def names_products_service():
    app.logger.info('Method names_products_service init')
    result = products
    app.logger.info('Method names_products_service ending')
    return result


def products_service(name):
    app.logger.info('Method products_service_get init')
    found = True
    try:
        result = read_json(name)
    except FileNotFoundError:
        result = []
        found = False
    app.logger.info('Method products_service_get ending')
    return result, found
