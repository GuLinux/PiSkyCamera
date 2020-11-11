from collections import namedtuple
import os

settings = {
    'resolution': (4056, 3040),
    'use_video_port': True,
    'city': 'London',
    'file_format': 'jpeg',
    'output_directory': os.path.join(os.environ['HOME'], 'timelapse'),
    'timelapse_seconds': 10,
    'profiles': {},
    'default_profile': { 'exposure': 0, 'iso': 100 },
    'symlink_latest': True,
    'jpeg_quality': 85,
}

# camera_profiles = {
#     'day':             { 'exposure': 0 , 'iso': 100 },
#     'twilight_bright': { 'exposure': 0 , 'iso': 200 },
#     'twilight':        { 'exposure': 0 , 'iso': 800 },
#     'night':           { 'exposure': 15, 'iso': 200, 'awb': (2.32421875, 2.41015625) },
# }



if os.path.isfile('local_settings.py'):
    import local_settings
    settings.update(local_settings.settings)

Settings = namedtuple('Settings', settings.keys())
settings = Settings(**settings)