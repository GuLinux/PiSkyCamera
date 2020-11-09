#!/usr/bin/env python3
from check_sun import CheckSun
from camera import Camera
import time
import os
import sys

output_directory = '/home/pi/timelapse'
timelapse_secs = 60

file_format='png'
file_ext = 'jpg' if file_format == 'jpeg' else file_format

time_format = '%Y-%m-%dT%H-%M-%S.{}'.format(file_ext)


camera_profiles = {
    'day':             { 'exposure': 0 , 'iso': 100, 'awb': None },
    'twilight_bright': { 'exposure': 0 , 'iso': 200, 'awb': None },
    'twilight':        { 'exposure': 0 , 'iso': 800, 'awb': None },
    'night':           { 'exposure': 15, 'iso': 200, 'awb': [2.32421875, 2.41015625] },
}

camera = Camera()
check_sun = CheckSun('London')
#camera.compute_awb()

latest_file = os.path.join(output_directory, 'latest.{}'.format(file_ext))
last_profile = None

while True:
    started = time.time()
    profile_name = check_sun.get_profile()
    profile = camera_profiles[profile_name]
    print('{}: {}'.format(profile_name, profile))

    if last_profile != profile_name:
        print('Switching profile : {} => {}'.format(last_profile, profile_name))
        last_profile = profile_name
        if not profile['awb']:
            print('Computing AWB for profile {}'.format(profile_name))
            camera.compute_awb()

    temp_file = '/tmp/timelapse_tmp.{}'.format(file_ext)
    camera.capture(profile['iso'], profile['exposure'], temp_file, format=file_format, awb_gains=tuple(profile['awb']))
    output_file = os.path.join(output_directory, time.strftime(time_format))
    os.rename(temp_file, output_file)
    if os.path.exists(latest_file):
        os.remove(latest_file)
    os.symlink(output_file, latest_file)
    finished = time.time()
    elapsed = finished - started
    sleep_time = max(0, timelapse_secs - elapsed)
    print('elapsed: {}, sleeping for: {}'.format(elapsed, sleep_time))
    time.sleep(sleep_time)

