from settings import settings
import time
from logger import logging
from PIL import Image, ImageFont, ImageDraw
from multiprocessing import Process


def pil_annotate(filename):
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(settings.pil_annotate_text_font, settings.pil_annotate_text_size)
    text = time.strftime(settings.pil_annotate_time_format) if settings.pil_annotate_time_format else settings.pil_annotate_text
    logging.debug('Annottating {} using text "{}" with PIL'.format(filename, text))
    draw.text(settings.pil_annotate_text_position, text, settings.pil_annotate_foreground,font=font)
    img.save(filename)



def pil_postprocess(filename):
    if settings.pil_annotate_text or settings.pil_annotate_time_format:
        p = Process(target=pil_annotate, args=(filename,))
        p.start()
