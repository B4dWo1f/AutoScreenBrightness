#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow import keras
import numpy as np
import datetime as dt
import cv2
import functions as funcs
import matplotlib.pyplot as plt

fmodel = 'auto_brightness.h5'

## Data
data = np.loadtxt('datos.dat',delimiter=',')
np.random.shuffle(data)   # shuffle rows

Nsamples = data.shape[0]
# Ntest = int(Nsamples*0.2)   # 20% of training used for testing
X_train = data[:,:-1]
Y_train = data[:,-1]
# X_test = data[-Ntest:,:-1]
# Y_test = data[-Ntest:,-1]

inp_shape = X_train[0].shape

# Load model or create a new one
try: model = keras.models.load_model(fmodel)
except OSError:
   model = keras.Sequential([
      keras.layers.Dense(30, activation='tanh',input_shape=inp_shape),
      keras.layers.Dense(20, activation='tanh'),
      keras.layers.Dense(1, activation=None)])

   model.compile(optimizer='adam',
                 loss='mse',
                 metrics=['accuracy'])


model.summary()

history = model.fit(X_train, Y_train, epochs=500, verbose=2)


# plot learning curve
err = history.history['loss']
acc = history.history['accuracy']
fig, ax = plt.subplots()
ax.plot(err,label='loss')
ax.plot(acc,label='accuracy')
ax.set_title('Learning curve')
ax.set_ylim(bottom=0)
plt.show()

########################################################################
max_bright = funcs.get_max_brightness()
brightness = funcs.get_brightness()

img = funcs.take_picture()
ImeanR,IvarR,IstdR,ImeanB,IvarB,IstdB,ImeanG,IvarG,IstdG = funcs.analyze_image(img)

img = funcs.take_screenshot()
SmeanR,SvarR,SstdR,SmeanB,SvarB,SstdB,SmeanG,SvarG,SstdG = funcs.analyze_image(img)
########################################################################

inp = np.array([[ImeanR,IvarR,IstdR, ImeanB,IvarB,IstdB, ImeanG,IvarG,IstdG,
                 SmeanR,SvarR,SstdR, SmeanB,SvarB,SstdB, SmeanG,SvarG,SstdG]])

prediction = model.predict(inp)
error = abs(brightness - prediction[0,0])
print('\n===================')
print('= Expected  :',int(brightness*max_bright))
print('= Calculated:',int(prediction[0,0]*max_bright))
print(f'= Error: {round(error*100,1)}%')
print('===================')

print(f'Saving model to {fmodel}')
model.save(fmodel)
print('Done!')
