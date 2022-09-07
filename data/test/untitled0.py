# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:29:38 2022

@author: jesus
"""
import os

import tensorflow as tf
from tensorflow import keras

new_model = tf.keras.models.load_model('product5.h5')
test = new_model.predict(200)
