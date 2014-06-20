"""
Various useful helpers.

"""

import os
from PIL import ExifTags, Image
from ghostscript import Ghostscript
from io import BytesIO
from tempfile import gettempdir, NamedTemporaryFile
from uuid import uuid4


TAGS = {value: key for key, value in list(ExifTags.TAGS.items())}


def pdf2png(pdf, size):
    """Transform a PDF to a PNG thumbnail."""
    temporary_name = os.path.join(gettempdir(), uuid4().hex)
    # Dump it to a temp file so that we can feed it to ghostscript
    # It would be cool to use gs.run_file, but it almost never works
    real_file = NamedTemporaryFile(delete=False)
    pdf.seek(0)
    real_file.write(pdf.read())
    real_file.close()
    args = [s.encode('utf-8') for s in [
        "",
        "-sstdout=/dev/null",
        "-dNOPAUSE", "-dBATCH", "-dSAFER",
        "-dFirstPage=1", "-dLastPage=1",
        "-dTextAlphaBits=4", "-dGraphicsAlphaBits=4",
        "-sDEVICE=png16m",
        "-r42",
        "-sOutputFile=%s" % temporary_name,
        "-f%s" % real_file.name]]
    Ghostscript(*args)
    os.remove(real_file.name)
    with open(temporary_name, 'rb') as f:
        img = BytesIO(f.read())
    os.remove(temporary_name)
    return image2png(img, size)


def image2png(file_, size):
    """Transform an image to a PNG thumbnail."""
    image = Image.open(file_)
    if hasattr(image, '_getexif'):
        info = image._getexif()
        # Apply EXIF transformation
        if info:
            orientation = info.get(TAGS['Orientation'])
            # This code proudly brought to you by a StackOverflow answer
            if orientation == 1:
                # Standard orientation
                pass
            elif orientation == 2:
                # Vertical image
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                # Rotation 180°
                image = image.transpose(Image.ROTATE_180)
            elif orientation == 4:
                # Horizontal image
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            elif orientation == 5:
                # Horizontal image + Rotation 270°
                image = image.transpose(
                    Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
            elif orientation == 6:
                # Rotation 270°
                image = image.transpose(Image.ROTATE_270)
            elif orientation == 7:
                # Vertical image + Rotation 270°
                image = image.transpose(
                    Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
            elif orientation == 8:
                # Rotation 90°
                image = image.transpose(Image.ROTATE_90)
    image.thumbnail(size, Image.ANTIALIAS)
    image_file = BytesIO()
    try:
        image.save(image_file, 'png')
    except IOError:
        image.save(image_file, 'jpeg')
    return image_file
