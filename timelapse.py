#!/usr/bin/env python3
from check_sun import CheckSun
from camera import Camera
import time
import os
import sys
from settings import settings
from logger import logging

logging.debug('Settings: {}'.format(settings))
file_ext = 'jpg' if settings.file_format == 'jpeg' else settings.file_format

camera = Camera(resolution=settings.resolution)
check_sun = CheckSun(settings.city)
#camera.compute_awb()


last_profile = None
output_file_format = os.path.join(settings.output_directory, '{timestamp:%Y-%m-%d-%H-%M-%S}.' + file_ext)

def symlink_latest(filename):
    latest_file = os.path.join(settings.output_directory, 'latest.{}'.format(file_ext))
    if os.path.islink(latest_file):
        os.remove(latest_file)
    os.symlink(filename, latest_file)

latest_capture = time.time()
for filename in camera.capture_continuous(output_file_format, format=settings.file_format):

    profile_name = check_sun.get_profile()
    profile = settings.profiles.get(profile_name, settings.default_profile)
    logging.debug('{}: {}'.format(profile_name, profile))

    if last_profile != profile_name:
        logging.info('Switching profile : {} => {}'.format(last_profile, profile_name))
        last_profile = profile_name
        if not profile.get('awb'):
            logging.debug('Computing AWB for profile {}'.format(profile_name))
            camera.compute_awb()
        camera.setup_capture(profile['iso'], profile['exposure'], profile.get('awb'), profile.get('exposure_mode', 'off'))



    finished = time.time()
    elapsed = finished - latest_capture 
    latest_capture = finished
    sleep_time = max(0, settings.timelapse_seconds - elapsed)
    logging.debug('{}, {}: elapsed: {}, sleeping for: {}'.format(profile_name, filename, elapsed, sleep_time))
    if settings.symlink_latest:
        symlink_latest(filename)
    time.sleep(sleep_time)



