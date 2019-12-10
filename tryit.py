#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
here = os.path.dirname(os.path.realpath(__file__))

import numpy as np
import datetime as dt
import cv2
import functions as funcs
import sys
# TF
import tensorflow as tf
from tensorflow import keras


try: fname = f'{here}/{sys.argv[1]}'
except IndexError:
   fname = f'{here}/auto_brightness.h5'
   if os.path.isfile(fname): print(f'No file specified, using {fname}')
   else:
      print('File not specified')
      exit()


model = keras.models.load_model(fname)

## Get inputs
brightness = funcs.get_brightness()
max_bright = funcs.get_max_brightness()

img = funcs.take_picture()
ImeanR,IvarR,IstdR,ImeanB,IvarB,IstdB,ImeanG,IvarG,IstdG = funcs.analyze_image(img)

img = funcs.take_screenshot()
SmeanR,SvarR,SstdR,SmeanB,SvarB,SstdB,SmeanG,SvarG,SstdG = funcs.analyze_image(img)

night_light = funcs.get_night_light_status()


inp = np.array([[ImeanR,IvarR,IstdR, ImeanB,IvarB,IstdB, ImeanG,IvarG,IstdG,
                 SmeanR,SvarR,SstdR, SmeanB,SvarB,SstdB, SmeanG,SvarG,SstdG,
                 night_light]])

prediction = model.predict(inp)
error = abs(brightness - prediction[0,0])
print('\n===================')
print(f'= Expected  : {int(brightness*max_bright)}')
print(f'= Calculated: {int((prediction[0,0]*(max_bright-1))+1)}')
print(f'= Error: {round(error*100,1)}%')
print('===================')

# com = f"echo {int(prediction[0,0]*max_bright)} | sudo tee /sys/class/backlight/intel_backlight/brightness"
# print('\nTry it with:')
# print(com)
com = funcs.set_brightness(int(prediction[0,0]*100))
print(com)
