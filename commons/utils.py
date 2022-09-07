from flask import Flask
import pandas as pd
import os
import json

app = Flask(__name__)

products = ['BOTANA',
            'DULCES',
            'ABARROTES',
            'BEBIDAS',
            'PANADERIA Y REPORTERIA',
            'LACTEOS Y EMBUTIDOS',
            'SERVICIOS Y LIMPIEZA',
            'FRUTAS Y VERDURAS',
            'QUESOS',
            'CARNES Y AVES',
            'ALMACEN COCINA',
            'SECOS Y CEREALES',
            'CERVEZAS',
            'CIGARROS',
            'PESCADOS Y MARISCOS',
            'ESPECIAS',
            'HELADOS',
            'VINOS Y LICORES']


def default_error(url, error):
    return {
        'url': url,
        'error': error
    }


def get_name_file(consulta=''):
    rute = 'data/product/'
    files = os.listdir(rute)
    for i in range(0, len(files)):
        dfr = pd.read_csv(rute+files[i], encoding='Latin-1', low_memory=False)
        descripcion = [v for v in dfr.Descripcion.unique()]
        if descripcion[0] == consulta:
            break
    return files[i]


def create_json(file, data):
    with open(f'products/{file}.json', 'w') as f:
        json.dump(data, f)


def read_json(file):
    with open(f'products/{file}.json') as f:
        json_data = json.load(f)
        return json_data['data']
