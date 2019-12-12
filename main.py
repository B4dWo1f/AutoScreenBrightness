#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow import keras
# from tensorflow.keras.callbacks import EarlyStopping
import numpy as np
import datetime as dt
import cv2
import functions as funcs
import matplotlib.pyplot as plt
from matplotlib import gridspec

fmodel = 'auto_brightness.h5'

## Data
data = np.loadtxt('datos.dat',delimiter=',')
np.random.shuffle(data)   # shuffle rows

train_inds = np.array([i for i in range(len(data)) if i%10!=0])
val_inds = np.array([i for i in range(len(data)) if i%10==0])


Nsamples = data.shape[0]
# Ntest = int(Nsamples*0.2)   # 20% of training used for testing
X_train = data[train_inds,:-1]
Y_train = data[train_inds,-1]
X_test = data[val_inds,:-1]
Y_test = data[val_inds,-1]

inp_shape = X_train[0].shape

# Load model or create a new one
try:
   model = keras.models.load_model(fmodel)
   print(f'Loaded model: {fmodel}')
except OSError:
   print('New model')
   model = keras.Sequential([
      keras.layers.Dense(10, activation='tanh',input_shape=inp_shape),
      keras.layers.Dense(5, activation='tanh'),
      keras.layers.Dense(1, activation=None)])

   model.compile(optimizer='adam',
                 loss='mse',
                 metrics=['accuracy'])


model.summary()

# es = EarlyStopping(monitor='val_loss', patience=100, verbose=1)

history = model.fit(X_train, Y_train, validation_data=(X_test, Y_test),
                                      epochs=500,
                                      verbose=2)
                                      # callbacks=[callback])


# plot learning curve
err = history.history['loss']
val_err = history.history['val_loss']
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

fig = plt.figure()  #figsize=(20,10))
gs = gridspec.GridSpec(2, 1)
fig.subplots_adjust(wspace=0.,hspace=0.15)
ax1 = plt.subplot(gs[0])  # Original plot
ax2 = plt.subplot(gs[1], sharex=ax1)  # dists

ax1.plot(err,label='loss')
ax1.plot(val_err,label='val_loss')
ax2.plot(acc,label='accuracy')
ax2.plot(val_acc,label='val_accuracy')
ax1.set_title('Learning curve')
ax1.set_ylim(bottom=0)
ax2.set_ylim(bottom=0)
ax1.legend()
ax2.legend()
plt.show()

########################################################################
max_bright = funcs.get_max_brightness()
brightness = funcs.get_brightness()

img = funcs.take_picture()
ImeanR,IvarR,IstdR,ImeanB,IvarB,IstdB,ImeanG,IvarG,IstdG = funcs.analyze_image(img)

img = funcs.take_screenshot()
SmeanR,SvarR,SstdR,SmeanB,SvarB,SstdB,SmeanG,SvarG,SstdG = funcs.analyze_image(img)

night_light = funcs.get_night_light_status()
########################################################################

inp = np.array([[ImeanR,IvarR,IstdR, ImeanB,IvarB,IstdB, ImeanG,IvarG,IstdG,
                 SmeanR,SvarR,SstdR, SmeanB,SvarB,SstdB, SmeanG,SvarG,SstdG,
                 night_light]])

prediction = model.predict(inp)
error = abs(brightness - prediction[0,0])*100/brightness
print('\n===================')
print('= Expected  :',int(brightness*max_bright))
print('= Calculated:',int(prediction[0,0]*max_bright))
print(f'= Error: {round(error,1)}%')
print('===================')

print(f'Saving model to {fmodel}')
model.save(fmodel)
print('Done!')
