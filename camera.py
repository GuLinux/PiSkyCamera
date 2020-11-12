from picamera import PiCamera
from picamera.color import Color
import time
from settings import settings
from logger import logging
from pil_postprocess import pil_postprocess


FRAMERATE_RANGE_DEFAULT = (0.005,15)
USE_VIDEO_PORT = True

class Camera:
    def __init__(self, resolution=(4056, 3040)):
        self.__picamera = PiCamera(resolution=resolution, sensor_mode=3)

    def compute_awb(self, iso=100, awb_mode='sunlight', shutter=0, seconds=5, exposure_mode='off'):
        self.__picamera.exposure_mode = 'auto'
        self.__picamera.awb_mode = awb_mode
        self.__picamera.iso = iso
        self.__picamera.shutter_speed = shutter
        time.sleep(seconds)
        awb_gains = self.__picamera.awb_gains
        self.__picamera.awb_mode = 'off'
        self.__picamera.exposure_mode = exposure_mode
        self.__picamera.awb_gains = awb_gains
        return awb_gains

    def capture(self, filename, format='jpeg'):
        self.__annotate_text()
        self.__picamera.capture(filename, **self.__capture_opts(format))
        pil_postprocess(filename)

    def capture_continuous(self, filename_format, format='jpeg'):
        self.__annotate_text()
        def generator():
            for filename in self.__picamera.capture_continuous(filename_format, **self.__capture_opts(format)):
                pil_postprocess(filename)
                yield filename
                self.__annotate_text()

        return generator()

    def __annotate_text(self):
        if settings.annotate_text:
            self.__picamera.annotate_text = settings.annotate_text
            logging.debug('Camera text annotation: {}'.format(self.__picamera.annotate_text))
        elif settings.annotate_time_format:
            timestamp_annotation = time.strftime(settings.annotate_time_format)
            self.__picamera.annotate_text = timestamp_annotation
            logging.debug('Camera timestamp annotation: {}'.format(timestamp_annotation))
        else:
            self.__picamera.annotate_text = None

    def __capture_opts(self, format):
        opts = {
            'format': format,
            'use_video_port': settings.use_video_port,
        }
        if format == 'jpeg':
            opts['quality'] = settings.jpeg_quality
        return opts

    def setup_capture(self, iso, shutter_speed, awb_gains, exposure_mode='off'):
        self.__picamera.awb_mode = 'off'
        self.__picamera.exposure_mode = exposure_mode
        if shutter_speed:
            self.__picamera.framerate = 1 / shutter_speed
        else:
            self.__picamera.framerate = 1
        if awb_gains:
            self.__picamera.awb_gains = awb_gains

        self.__picamera.shutter_speed = int(shutter_speed * 1000 * 1000)
        self.__picamera.iso = iso
        if settings.annotate_background:
            self.__picamera.annotate_background = Color(settings.annotate_background)
        if settings.annotate_foreground:
            self.__picamera.annotate_foreground = Color(settings.annotate_foreground)
        if settings.annotate_text_size:
            self.__picamera.annotate_text_size = settings.annotate_text_size

