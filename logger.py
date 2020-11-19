import logging
from settings import settings

logging.basicConfig(level=settings.log_level, format='%(asctime)s %(message)s')
