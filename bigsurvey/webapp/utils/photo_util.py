from time import strftime
from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile
import os


THUMBNAIL_SIZE = 300, 300


# required for renaming file on upload
def rename(instance, filename):
    ext = filename.split('.')[-1]
    return 'photo/{}.{}'.format(strftime("%Y%m%d-%H%M%S"), ext)


def create_thumbnail(image):
    pil_type = 'jpeg'
    image_type = 'image/jpeg'
    if image.name.split('.')[-1] == 'png':
        pil_type = 'png'
        image_type = 'image/png'
    thumb_image = Image.open(StringIO(image.read()))
    thumb_image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    thumb_file = StringIO()
    thumb_image.save(thumb_file, pil_type)
    thumb_file.seek(0)
    thumb = SimpleUploadedFile(os.path.split(image.name)[-1], thumb_file.read(), content_type=image_type)
    return thumb
