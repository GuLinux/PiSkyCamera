#!/usr/bin/env python3
from check_sun import CheckSun
from camera import Camera
import time
import os
import shutil
import sys
from settings import settings
from logger import logging

logging.debug('Settings: {}'.format(settings))

camera = Camera(resolution=settings.resolution)
check_sun = CheckSun(settings.city)
#camera.compute_awb()


last_profile = None
output_file_format = os.path.join(settings.output_directory, '{}.{}'.format(settings.file_timestamp_format, settings.file_ext))
os.makedirs(settings.output_directory, exist_ok=True)
if settings.move_to_directory:
    os.makedirs(settings.move_to_directory, exist_ok=True)


def symlink_latest(filename):
    if os.path.islink(settings.latest_path):
        os.remove(settings.latest_path)
    os.symlink(filename, settings.latest_path)


while True:
    filename = time.strftime(output_file_format)

    profile_name = check_sun.get_profile()
    profile = settings.profiles.get(profile_name)
    logging.debug('{}: {}{}'.format(profile_name, profile, '' if profile else ' - profile undefined, using default: {}'.format(settings.default_profile)))
    if not profile:
        profile_name = 'default'
        profile = settings.default_profile

    if last_profile != profile_name:
        logging.info('Switching profile : {} => {}'.format(last_profile, profile_name))
        last_profile = profile_name
        if not profile.get('awb'):
            logging.debug('Computing AWB for profile {}'.format(profile_name))
            camera.compute_awb()
        camera.setup_capture(profile['iso'], profile['exposure'], profile.get('awb'), profile.get('exposure_mode', 'off'))

    latest_capture = time.time()
    camera.capture(filename, format=settings.file_format, use_video_port=profile.get('use_video_port'))

    finished = time.time()
    elapsed = finished - latest_capture 

    sleep_time = max(0, settings.timelapse_seconds - elapsed)
    logging.debug('{}, {}: elapsed: {}, sleeping for: {}'.format(profile_name, filename, elapsed, sleep_time))

    if settings.symlink_latest:
        symlink_latest(filename)

    time.sleep(sleep_time)

