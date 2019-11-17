#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
This script will take a picture and a screenshot every time the user changes the
screen brightness and record some analysis to a file
"""

import numpy as np
import cv2
import datetime as dt
import os
here = os.path.dirname(os.path.realpath(__file__))
import functions as funcs
from time import sleep

data_file = f'{here}/datos.dat'
brigtness_file = '/sys/class/backlight/intel_backlight/brightness'
stop_file = f'{here}/STOP'
t0 = 3

brightness = funcs.get_brightness()
old = brightness
while not os.path.isfile(stop_file):
   while old == brightness and not os.path.isfile(stop_file):
      brightness = funcs.get_brightness()
      if brightness != old: break
      sleep(t0)
   old = brightness
   # Brightness has changed. Take picture and screenshot

   # # Time of the day
   # seconds_since_midnight = funcs.second_of_the_day()

   # Take picture from webcam
   img = funcs.take_picture()
   ImeanR,IvarR,IstdR,ImeanB,IvarB,IstdB,ImeanG,IvarG,IstdG = funcs.analyze_image(img)

   # Take screenshot
   img = funcs.take_screenshot()
   SmeanR,SvarR,SstdR,SmeanB,SvarB,SstdB,SmeanG,SvarG,SstdG = funcs.analyze_image(img)

   # Write data
   with open(data_file,'a') as f:
      # f.write(f'{seconds_since_midnight},')
      f.write(f'{ImeanR},{IvarR},{IstdR},')
      f.write(f'{ImeanB},{IvarB},{IstdB},')
      f.write(f'{ImeanG},{IvarG},{IstdG},')
      f.write(f'{SmeanR},{SvarR},{SstdR},')
      f.write(f'{SmeanB},{SvarB},{SstdB},')
      f.write(f'{SmeanG},{SvarG},{SstdG},')
      f.write(f'{brightness}\n')
