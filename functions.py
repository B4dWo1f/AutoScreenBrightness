#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import datetime as dt
import os

def analyze_image(img):
   # Red
   meanR = round(np.mean(img[:,:,0]),4)
   varR  = round(np.var(img[:,:,0]),4)
   stdR  = round(np.std(img[:,:,0]),4)
   # Blue
   meanB = round(np.mean(img[:,:,1]),4)
   varB  = round(np.var(img[:,:,1]),4)
   stdB  = round(np.std(img[:,:,1]),4)
   # Green
   meanG = round(np.mean(img[:,:,2]),4)
   varG  = round(np.var(img[:,:,2]),4)
   stdG  = round(np.std(img[:,:,2]),4)
   return meanR, varR, stdR, meanB, varB, stdB, meanG, varG, stdG


def take_picture(vid_device=0,pre=30,norm=True):
   """
   Take a picture from webcam using cv2
   vid_device: index of video device as in /dev/video*
   pre: number of pictures to take BEFORE final picture. This serves as camera
        warm up time
   norm: whether to return the image normalized to 0-1
   """
   # Take picture from webcam
   cam = cv2.VideoCapture(vid_device)
   for i in range(pre):
      ret, img = cam.read()
   cam.release()
   cv2.destroyAllWindows 
   if norm: return img/255
   else: return img


def take_screenshot(ftmp='/tmp/screenshot.png',delete=True,norm=True):
   """
   Take a screenshot
   ftmp: temporary name of the file
   delete: delete the file after the screenshot
   norm: whether to return the image normalized to 0-1
   """
   # Take screenshot
   com = f'import -window root {ftmp}'
   os.system(com)
   img = cv2.imread(ftmp)
   if delete: os.system(f'rm {ftmp}')
   if norm: return img/255
   else: return img


def second_of_the_day(norm=True):
   """
   Returns the seconds elapsed since midnight.
   norm: normalizes it to the interval 0-1
   """
   # Time of the day
   now = dt.datetime.now()
   midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
   seconds_since_midnight = (now - midnight).total_seconds()
   seconds_since_midnight = round(seconds_since_midnight ,6)
   if norm: seconds_since_midnight = seconds_since_midnight/(24*60*60)
   return round(seconds_since_midnight,6)


def get_max_brightness():
   fol = '/sys/class/backlight/intel_backlight/'
   max_bright = fol + '/max_brightness'
   max_bright = open(max_bright,'r').read().strip()
   return int(max_bright)

def get_brightness(norm=True):
   fol = '/sys/class/backlight/intel_backlight/'
   brigtness_file = fol + '/brightness'
   brightness = open(brigtness_file,'r').read().strip()
   max_bright = get_max_brightness()
   brightness = int(brightness)
   if norm: return brightness/max_bright
   else: return brightness
