from flask import Flask
from services.products_service import products_service
from services.products_service import names_products_service
from commons.utils import default_error


app = Flask(__name__)
message = ''
status_code = 0


def names_products_controller():
    app.logger.info('Method names_products_controller_get init')
    result = names_products_service()
    message = {
        'data': result
    }
    app.logger.info('Method names_products_controller_get ending')
    return message


def seacrh_products_controller(body):
    app.logger.info('Method seacrh_products_controller_get init')
    found = True
    status_code = 200
    if ('product' not in body):
        message = default_error(
            '/seacrh-products', 'the product field is required')
        status_code = 400
    else:
        message, found = products_service(body['product'])
    result = {
        'data': message
    }
    if (found == False):
        result['details'] = f'the product: {body["product"]} not exist'
    app.logger.info('Method seacrh_products_controller_get ending')
    return result, status_code
