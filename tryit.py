#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import numpy as np
import datetime as dt
import cv2
import functions as funcs
# TF
import tensorflow as tf
from tensorflow import keras

fname = 'auto_brightness.h5'

model = keras.models.load_model(fname)

## Get inputs
brightness = funcs.get_brightness()
max_bright = funcs.get_max_brightness()

img = funcs.take_picture()
ImeanR,IvarR,IstdR,ImeanB,IvarB,IstdB,ImeanG,IvarG,IstdG = funcs.analyze_image(img)

img = funcs.take_screenshot()
SmeanR,SvarR,SstdR,SmeanB,SvarB,SstdB,SmeanG,SvarG,SstdG = funcs.analyze_image(img)


inp = np.array([[ImeanR,IvarR,IstdR, ImeanB,IvarB,IstdB, ImeanG,IvarG,IstdG,
                 SmeanR,SvarR,SstdR, SmeanB,SvarB,SstdB, SmeanG,SvarG,SstdG]])

B = model.predict(inp)
print('Current_brightness:',int(brightness*max_bright))
print('suggested:',B*max_bright)

com = f"echo {int(B[0,0]*max_bright)} | sudo tee /sys/class/backlight/intel_backlight/brightness"
print('\nTry it with:')
print(com)
