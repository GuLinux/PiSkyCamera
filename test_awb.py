#!/usr/bin/env python3
from camera import Camera
import sys

def to_dec(fraction):
    return fraction.numerator / fraction.denominator

camera = Camera()
try:
    awb_gains = camera.compute_awb(iso=int(sys.argv[1]), awb_mode=sys.argv[2], shutter=int(sys.argv[3]) * 1000*1000, seconds=int(sys.argv[4]))
    print(awb_gains)
    print(to_dec(awb_gains[0]), to_dec(awb_gains[1]))
except:
    print('Usage: {} ISO awb_mode shutter_secs seconds_wait'.format(sys.argv[0]))


