from PIL import Image
from io import BytesIO
import shutil
import tempfile

MOCK_MEDIA_ROOT = tempfile.mkdtemp()


class ImageFactory():
    def getImage(self):
        image = Image.new('RGB', size=(50, 50), color=(128, 11, 2))
        image_file = BytesIO()
        image.save(image_file, 'JPEG')  # or whatever format you prefer
        image_file.seek(0)
        return image_file

    def cleanUp(self):
        shutil.rmtree(MOCK_MEDIA_ROOT, ignore_errors=True)
