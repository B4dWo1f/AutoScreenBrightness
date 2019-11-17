# Auto-Brightness

If your computer doesn't have an Ambient Light Sensor (ALS), this code should work around that to offer automatic dimming based on surrounding light and screen
content.

It collects data for N days where the user manually controls the brightness, after that period a NN is trained to predict the desired brightness at any given time.

## requirements
ubuntu (should be easy to export to other OSs)
tensorflow 2.0
opencv 3.2 (sudo apt-get install python3-opencv is fine on ubuntu 18.04)
