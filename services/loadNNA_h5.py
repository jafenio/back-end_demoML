# LSTM  para predecir a los productos de COUNTRY
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from pandas import read_csv
import numpy
import math
import tensorflow as tf
# convertimos un array de valores en una matriz de conjuntos de datos
# hardcode
plot = True


def create_dataset(dataset, look_back=1):
    data_x, data_y = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        data_x.append(a)
        data_y.append(dataset[i + look_back, 0])
    return numpy.array(data_x), numpy.array(data_y)


def predictor(directory, name, mm):
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
    print('Resultado del entrenamiento: %.2f RMSE' % (train_score))
    test_score = math.sqrt(mean_squared_error(test_y[0], test_predict[:, 0]))
    print('Resultado del test: %.2f RMSE' % (test_score))
    return dataset, test_predict, train_predict, train_score
