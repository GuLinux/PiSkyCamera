from settings import settings
import time
from logger import logging
from PIL import Image, ImageFont, ImageDraw
from multiprocessing import Process

pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)

def pil_process(filename):
    img = Image.open(filename)
    pil_annotate(img)
    pil_save_preview(img)
    img.save(filename)

def pil_annotate(img):
    if settings.pil_annotate_text or settings.pil_annotate_time_format:
        started = time.time()
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(settings.pil_annotate_text_font, settings.pil_annotate_text_size)
        text = time.strftime(settings.pil_annotate_time_format) if settings.pil_annotate_time_format else settings.pil_annotate_text
        draw.text(settings.pil_annotate_text_position, text, settings.pil_annotate_foreground,font=font)
#       logging.debug('pil_annotate: file={}, text="{}", elapsed: {}'.format(filename, text, time.time() - started))


def pil_save_preview(img):
    if settings.pil_save_preview:
        filename = os.path.join(settings.output_directory, settings.pil_save_preview['filename'])
        quality = settings.pil_save_preview.get('quality', 75)
        resolution = settings.pil_save_preview.get('resolution', img.size)
        resized = img.resize(resolution)
        resized = resized.convert('RGB')
        resized.save(filename, quality=quality)


def pil_postprocess(filename):
    if settings.pil_annotate_text or settings.pil_annotate_time_format or settings.pil_save_preview:
        p = Process(target=pil_process, args=(filename,))
        p.start()
