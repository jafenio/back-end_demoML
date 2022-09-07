from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from commons.utils import default_error
from controller.products_controller import names_products_controller
from controller.products_controller import seacrh_products_controller
from controller.prediction_controller import prediction_product_controller
import json

app = Flask(__name__)
CORS(app)


path_url = '/msdemo/v1'


def body_response(body={}, status=200):
    return Response(
        json.dumps(body, default=str),
        mimetype="application/json",
        status=status
    )


@app.route(f'{path_url}/')
def home_page():
    return jsonify(hello='world')


@app.route(f'{path_url}/category-products', methods=['GET'])
def category_products():
    app.logger.info('Method category_products init')
    message = names_products_controller()
    result = body_response(message, 200)
    app.logger.info('Method category_products ending')
    return result


@app.route(f'{path_url}/seacrh-products', methods=['POST'])
def seacrh_products():
    app.logger.info('Method seacrh_products init')
    body = dict(request.json)
    message, status_code = seacrh_products_controller(body)
    result = body_response(message, status_code)
    app.logger.info('Method seacrh_products ending')
    return result

@app.route(f'{path_url}/prediction-product', methods=['POST'])
def prediction_product():
    app.logger.info('Method prediction_product init')
    body = dict(request.json)
    message, status_code = prediction_product_controller(body)
    result = body_response(message, status_code)
    app.logger.info('Method prediction_product ending')
    return result


@app.errorhandler(404)
def not_found(error=None):
    app.logger.info('Error: not_found')
    message = default_error(request.url, error)
    app.logger.error(message)
    result = body_response(message, 404)
    return result


@app.errorhandler(405)
def method_not_allowed(error=None):
    app.logger.info('Error: method_not_allowed')
    message = default_error(request.url, error)
    app.logger.error(message)
    result = body_response(message, 405)
    return result


@app.errorhandler(400)
def method_bat_request(error=None):
    app.logger.info('Error: method_bat_request')
    message = default_error(request.url, error)
    app.logger.error(message)
    result = body_response(message, 400)
    return result

