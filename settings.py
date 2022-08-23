from collections import namedtuple
import json
import logging
import os

settings = {
    'resolution': (4056, 3040),
    'capture_timeout': None,
    'city': 'London',
    'file_format': 'jpeg',
    'output_directory': os.path.join(os.environ['HOME'], 'timelapse'),
    'move_to_directory': None,
    'timelapse_seconds': 10,
    'profiles': {},
    'file_timestamp_format': '%Y-%m-%dT%H-%M-%S',
    'default_profile': { 'exposure': 0, 'iso': 100, 'exposure_mode': 'auto', 'use_video_port': False },
    'symlink_latest': True,
    'copy_latest': False,
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

settings['file_ext'] = 'jpg' if settings.get('file_format') == 'jpeg' else settings.get('file_format')
settings['latest_path'] = os.path.join(settings['output_directory'], 'latest.{}'.format(settings['file_ext']))
settings['preview_path'] = os.path.join(settings['output_directory'], settings['pil_save_preview']['filename']) if settings['pil_save_preview'] and 'filename' in settings['pil_save_preview'] else None



print(f'Loaded settings: \n{json.dumps(settings, indent=4)}')
Settings = namedtuple('Settings', settings.keys())
settings = Settings(**settings)


