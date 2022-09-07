from flask import Flask
from commons.utils import get_name_file
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from pandas import read_csv
import numpy
import math
import tensorflow as tf
import pandas as pd

app = Flask(__name__)

plot = True


def create_dataset(dataset, look_back=1):
    app.logger.info('Method create_dataset init')
    data_x, data_y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        data_x.append(a)
        data_y.append(dataset[i + look_back, 0])
    app.logger.info('Method create_dataset ending')
    return numpy.array(data_x), numpy.array(data_y)


def predictor(directory, name, mm):
    app.logger.info('Method predictor init')
    input_set = directory + '/' + name
    # semilla aleatoria para reproducibilidad
    numpy.random.seed(7)
    # cargamos el conjunto de datos
    dataframe = read_csv(input_set,
                         usecols=['Actual'], engine='python', skipfooter=3)
    dataset = dataframe.values
    dataset = dataset.astype('float32')
    # normalizamos el conjunto de datos
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)
    # dividimos entre entranmiento y test
    train_size = int(len(dataset) * 0.67)
    train, test = dataset[0:train_size, :], dataset[train_size:len(dataset), :]
    # remodelamos X=t y Y=t+1
    look_back = 1
    train_x, train_y = create_dataset(train, look_back)
    test_x, test_y = create_dataset(test, look_back)
    # remodelamos la entrada para que sea[muestras, pasos de tiempo, características]
    train_x = numpy.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
    test_x = numpy.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))
    # cargamoss la LSTM network
    model = tf.keras.models.load_model(mm)
    # hacemos las predicciones
    train_predict = model.predict(train_x)
    test_predict = model.predict(test_x)
    # invertimos las predicciones
    train_predict = scaler.inverse_transform(train_predict)
    dataset = scaler.inverse_transform(dataset)
    train_y = scaler.inverse_transform([train_y])
    test_predict = scaler.inverse_transform(test_predict)
    test_y = scaler.inverse_transform([test_y])
    # calculamos el error rms
    train_score = math.sqrt(mean_squared_error(
        train_y[0], train_predict[:, 0]))
    app.logger.info('Resultado del entrenamiento: %.2f RMSE' % (train_score))
    test_score = math.sqrt(mean_squared_error(test_y[0], test_predict[:, 0]))
    app.logger.info('Resultado del test: %.2f RMSE' % (test_score))
    app.logger.info('Method predictor ending')
    return dataset, test_predict, train_predict, train_score


def prediction_service(product):
    app.logger.info('Method prediction_service init')
    ruta_in = 'data/product/'
    file = get_name_file(product)
    my_model = 'data/test/'+file[:-4]+'.h5'
    dfr = pd.read_csv('data/product/'+file, encoding='Latin-1')
    dia = dfr['Fecha']
    data_set, prediccion, entrenamiento, train_score = predictor(
        ruta_in, file, my_model)
    data_n = data_set.flatten()
    predict = prediccion.flatten()
    training = entrenamiento.flatten()
    zeros = numpy.zeros((len(training), 1))
    temp = predict.reshape(-1, 1)
    mespredict = numpy.concatenate((zeros, temp), axis=0)
    mespredict = mespredict.flatten()
    error_medio = round(train_score, 2)
    result = {
        'name': product,
        'mean-square-error': error_medio,
        'days': list(dia),
        'real-values': list(data_n),
        'training-values': list(training),
        'prediction-values': list(mespredict)
    }
    app.logger.info(f'days : {len(result["days"])}')
    app.logger.info(f'real-values : {len(result["real-values"])}')
    app.logger.info(f'training-values : {len(result["training-values"])}')
    app.logger.info(f'prediction-values : {len(result["prediction-values"])}')
    app.logger.info('Method prediction_service ending')
    return result

