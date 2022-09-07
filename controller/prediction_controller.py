from flask import Flask
from services.prediction_service import prediction_service
from commons.utils import default_error

app = Flask(__name__)
URL = 'http://localhost:5000'
message = ''
status_code = 0

def prediction_product_controller(body):
    app.logger.info('Method prediction_product_controller init')
    if ('product' not in body):
        message = default_error(
            f'{URL}/prediction-product', 'the product field is required')
        status_code = 400
    else:
        message = prediction_service(body['product'])
        status_code = 200
    message = {
        'data': message
    }
    app.logger.info('Method prediction_product_controller ending')
    return message, status_code