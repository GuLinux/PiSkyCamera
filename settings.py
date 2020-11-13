from collections import namedtuple
import logging
import os

settings = {
    'resolution': (4056, 3040),
    'city': 'London',
    'file_format': 'jpeg',
    'output_directory': os.path.join(os.environ['HOME'], 'timelapse'),
    'timelapse_seconds': 10,
    'profiles': {},
    'default_profile': { 'exposure': 0, 'iso': 100, 'exposure_mode': 'auto', 'use_video_port': False },
    'symlink_latest': True,
    'jpeg_quality': 85,
    'annotate_background': None,
    'annotate_foreground': None,
    'annotate_text_size': None,
    'annotate_text': None,
    'annotate_time_format': None,
    'log_level': logging.WARNING,
    'pil_annotate_foreground': (255,255,255),
    'pil_annotate_text_size': 10,
    'pil_annotate_text_font': 'sans-serif.ttf',
    'pil_annotate_text': None,
    'pil_annotate_time_format': None,
    'pil_annotate_text_position': (0,0),
    'pil_save_preview': None,
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
