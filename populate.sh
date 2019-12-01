#!/bin/bash

#
# Populate the trainig samples with the current brightness settings
#

REP=50
N=`cat /sys/class/backlight/intel_backlight/brightness`
N1=$((N+1))

for i in `seq $REP`
do
   echo $N
   echo $N | sudo tee /sys/class/backlight/intel_backlight/brightness
   sleep 10
   echo $N1
   echo $N1 | sudo tee /sys/class/backlight/intel_backlight/brightness
   sleep 10
done
