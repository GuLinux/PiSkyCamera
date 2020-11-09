from picamera import PiCamera
import time

class Camera:
    def __init__(self, resolution=(4056, 3040)):
        self.__picamera = PiCamera(resolution=resolution, framerate_range=(0.005,15), sensor_mode=3)

    def compute_awb(self, iso=100, awb_mode='sunlight', seconds=5):
        self.__picamera.exposure_mode = 'auto'
        self.__picamera.awb_mode = awb_mode
        self.__picamera.iso = iso
        time.sleep(seconds)
        self.__awb_gains = self.__picamera.awb_gains
        self.__picamera.awb_mode = 'off'
        self.__picamera.awb_gains = self.__awb_gains
        self.__picamera.exposure_mode = 'off'


    def capture(self, iso, shutter_speed, filename, format='jpeg'):
        self.__picamera.shutter_speed = int(shutter_speed * 1000 * 1000)
        self.__picamera.iso = iso
        self.__picamera.capture(filename, format=format)
